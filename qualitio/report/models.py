import re
import pickle

from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.db import models
from django.views import debug
from django.db.models import query
from django.template.defaultfilters import slugify

from qualitio import core
from qualitio.report.validators import report_query_validator


class RestrictedManager(models.Manager):
    # TODO: this class is not used, but should be included
    # in future as replacment for orginal managers
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

    class Meta:
        verbose_name_plural = 'Report directories'


class Report(core.BasePathModel):
    template = models.TextField(blank=True)
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
        for_parent_unique = True

    @property
    def context_dict(self):
        context_dict = {}
        for context_element in self.context.all():
           context_dict[context_element.name] = context_element.query_object()
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

    def save(self, *args, **kwargs):
        """
        save method makes ability setup 'query_pickled' field with user own value.
        Usefull then set of ContextElement objects are created / edited.
        See qualitio.report.forms.ContextElementFormset.save method.
        """
        query_result = kwargs.pop('query_result', None)
        if query_result:
            self.query_pickled = self.pickle_query_result(query_result)
        return super(ContextElement, self).save(*args, **kwargs)

    def full_clean(self):
        """
        full_clean starts the base class full_clean validation and
        also adds 'clean_query' validation.

        Construction of the method looks like this, because 'full_clean'
        should return ALL validation errors, not just a part.
        """
        errors = {}

        try:
            super(ContextElement, self).full_clean()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        try:
            self.clean_query()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def clean_query(self):
        """
        clean_query does two things
        1) it validates query string
        2) it syncronize evaluated query with 'query_pickled' attribute.
        """
        self.query_pickled = self.pickle_query_result(report_query_validator.clean(self.query))

    def pickle_query_result(self, result):
        if isinstance(result, query.QuerySet):
            result = result.__getstate__()
            result["_result_cache"] = None
        return pickle.dumps(result)

    def query_object(self):
        query_dict = pickle.loads(str(self.query_pickled))
        if not isinstance(query_dict, dict):
            return query_dict

        _query = query.QuerySet()
        _query.__dict__ = query_dict
        return _query
