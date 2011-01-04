from django.db import models
from qualitio.core import models as core

class TestCaseDirectory(core.BaseDirectoryModel):
    pass


class TestCase(core.BasePathModel):
    parent = models.ForeignKey('TestCaseDirectory', null=True, blank=True)
    requirement = models.ForeignKey('requirements.Requirement', null=True, blank=True)
    
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    precondition = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name


class TestCaseStep(core.BaseModel):
    testcase = models.ForeignKey('TestCase')
    description = models.TextField()
    expected = models.TextField(blank=True)
    sequence = models.PositiveIntegerField(null=True, default=0)
    
    class Meta:
        ordering = ['sequence']

class Attachment(core.BaseModel):
    testcase = models.ForeignKey('TestCase')
    name = models.CharField(max_length=512)
    attachment = models.FileField(upload_to="attachments")
