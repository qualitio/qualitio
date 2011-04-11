import re

from django.db import models
from django.template import Context, Template

from qualitio import core


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


# TODO: Proxy nad typem obiektem http://docs.djangoproject.com/en/1.3/topics/db/models/#proxy-models
class ReportDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class Report(core.BasePathModel):
    template = models.TextField(blank=True)

    class Meta(core.BasePathModel.Meta):
        parent_class = 'ReportDirectory'

    @property
    def context_dict(self):
        context_dict = {}
        for context_element in self.context.all():
           context_dict[context_element.name] = context_element.query_object

        return context_dict

    def content(self):
        template = Template(self.template)
        context = Context(self.context_dict)
        return template.render(context)


class ContextElement(models.Model):
    report = models.ForeignKey("Report", related_name="context")
    name = models.CharField(max_length=512)
    query = models.TextField()

    def query_object(self):
        from qualitio.store.models import TestCase
        from qualitio.execute.models import TestCaseRun, TestRun
        return eval(self.query, {"__builtins__": None}, {'TestCase': TestCase,
                                                         'TestCaseRun': TestCaseRun,
                                                         'TestRun' : TestRun,
                                                         'Report': Report})

