from django.db import models
from qualitio.core import models as core

class TestCaseDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestCase(core.BasePathModel):
    #TODO: move parent attribute to BasePathModel
    parent = models.ForeignKey('TestCaseDirectory', null=True, blank=True, related_name="subchildren")
    requirement = models.ForeignKey('requirements.Requirement', null=True, blank=True)
    
    description = models.TextField(blank=True)
    precondition = models.TextField(blank=True)


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
