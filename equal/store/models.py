from django.db import models
from mptt.models import MPTTModel


class TestCaseDirectory(MPTTModel):
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
        return '%s%s' % (self.get_path(),self.name)


class TestCase(models.Model):
    directory = models.ForeignKey('TestCaseDirectory', null=True, blank=True)

    name = models.CharField(max_length=512)
    precondition = models.TextField(blank=True)

    def get_path(self):
        return "%s%s/" % (self.directory.get_path(),
                         self.directory.name)


class TestCaseStep(models.Model):
    testcase = models.ForeignKey('TestCase')
    description = models.TextField()
    expected = models.TextField()
    

class Attachment(models.Model):
    testcase = models.ForeignKey('TestCase')
    name = models.CharField(max_length=512)
    attachment = models.FileField(upload_to="attachments")
