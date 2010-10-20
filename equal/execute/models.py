from django.db import models
from mptt.models import MPTTModel

class TestRunDirectory(MPTTModel):
    parent = models.ForeignKey('self', null=True, blank=True)

    name = models.CharField(max_length=512)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return "/execute/testrun/" % self.id

    def get_path(self):
        if self.get_ancestors():
            return "/%s/" % "/".join(map(lambda x: x.name, self.get_ancestors()))
        return "/"

    def __unicode__(self):
        return 'TestRunDirectory: %s' % self.name


class TestRun(models.Model):
    directory = models.ForeignKey('TestRunDirectory')

    name = models.CharField(max_length=512)

    def get_path(self):
        return "%s%s/" % (self.directory.get_path(),
                         self.directory.name)

class TestCaseRun(models.Model):
    name = models.CharField(max_length=512)
    testrun = models.ForeignKey('TestRun')


class Status(models.Model):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=512, blank=True)
