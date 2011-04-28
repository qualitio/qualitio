import re
import pickle

from django.core.exceptions import FieldError
from django.db import models
from django.template import Context, Template
from django.core.exceptions import ValidationError
from django.db.models import query, loading
from django.template.defaultfilters import slugify

from qualitio import core

import validators

class RestrictedManager(models.Manager):

    allowed_methods = ("_set_creation_counter", "get_query_set", "model", "_db", "__class__"
                       "contribute_to_class", "_inherited", "creation_counter",
                       "^get(\(.*\))?$",
                       "^filter(\(.*\))?$",
                       "^all(\(.*\))?$")

    def __getattribute__(self, name):
        if any(filter(lambda x: re.match(x,name), object.__getattribute__(self, "allowed_methods"))):
            return object.__getattribute__(self, name)

        raise AttributeError


class ReportDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class Report(core.BasePathModel):
    template = models.TextField(blank=True, validators=[validators.template_validate])
    public = models.BooleanField()
    link = models.URLField(blank=True, verify_exists=False)
    MIME_CHOICES = (('text/html', 'html'),
                    ('application/xml', 'xml'),
                    ('application/json', 'json'),
                    ('text/plain', 'plain'))
    mime = models.CharField(blank=False, max_length=20, choices=MIME_CHOICES,
                            default="text/html", verbose_name="format")

    class Meta(core.BasePathModel.Meta):
        parent_class = 'ReportDirectory'

    @property
    def context_dict(self):
        context_dict = {}
        for context_element in self.context.all():
           context_dict[context_element.name] = context_element.query_object

        return context_dict

    @property
    def content(self):
        template = Template(self.template)
        context = Context(self.context_dict)
        return template.render(context)

    def is_html(self):
        return self.mime == "text/html"

    def save(self, *args, **kwargs):
        # significant part of this link is only ID, rest is only for information purposes.
        # Filter applayed to get rid root's empty path
        if not self.pk:
            super(Report, self).save(*args, **kwargs)

        link_elements = filter(lambda x:x, [str(self.pk),
                                            slugify(self.parent.path),
                                            slugify(self.parent.name),
                                            slugify(self.name),
                                            self.created_time.strftime("%Y/%m/%d")])

        self.link = "/".join(link_elements)
        kwargs['force_insert'] = False
        super(Report, self).save(*args, **kwargs)


class ContextElement(models.Model):
    report = models.ForeignKey("Report", related_name="context")
    name = models.CharField(max_length=512)
    query = models.TextField()
    query_pickled = models.TextField(blank=True)

    ALLOWED_OBJECTS = ["TestCase", "TestCaseRun", "TestRun", "Report"]
    ALLOWED_METHODS = ["all", "get", "filter", "exclude", "order_by"]

    def query_object(self):
        return pickle.loads(str(self.query_pickled))


    def clean(self):
        query_segments  = self.query.split(".")
        if len(query_segments) < 2:
            raise ValidationError({"query": "Minimal query should be: ObjectType.method([key=value])"})

        valid_object = query_segments[0]
        methods = query_segments[1:]

        if valid_object not in self.ALLOWED_OBJECTS:
            raise ValidationError({"query": "Type '%s' is not supported" % valid_object})

        valid_methods = []
        for method in methods:
            method_re = re.match("(?P<method>\w+)\((?P<args>(\w+=.+)?)\)$", method)

            try:
                method_name = method_re.groupdict()["method"]
                try:
                    args = dict([(method_re.groupdict()["args"].split("=")[0],
                                  method_re.groupdict()["args"].split("=")[1].strip('"').strip("'"))])

                except IndexError:
                    args = dict()

            except AttributeError:
                raise ValidationError({"query": "Method '%s' is in wrong format" % method})

            if method_name not in self.ALLOWED_METHODS:
                raise ValidationError({"query": "Method '%s' is unsupported" % method_name})


            valid_methods.append((method_name, args))

        self.query_pickled = pickle.dumps(self._build_query(valid_object, valid_methods))


    @classmethod
    def _build_query(cls, object_name, methods):

        apps = ["requirements", "store", "execute", "report"]

        Object = None
        while not Object and apps:
            Object = loading.get_model(apps.pop(), object_name)

        if not Object:
            return query.QuerySet()

        query_set = Object.objects
        for name, kwargs in methods:
            try:
                query_set = getattr(query_set, name)(**kwargs)
            except Object.DoesNotExist:
                return None
            except FieldError as e:
                raise ValidationError({"query": repr(e) })


        return query_set
