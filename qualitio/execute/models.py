from django.db import models
from qualitio.core import models as core

class TestRunDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestRun(core.BasePathModel):
    parent = models.ForeignKey('TestRunDirectory', related_name="subchildren")

    notes = models.TextField(blank=True)


class TestCaseRun(core.BaseModel):
    parent = models.ForeignKey('TestRun', null=True, blank=True, related_name="subchildren")
    requirement = models.ForeignKey('requirements.Requirement', null=True, blank=True)
    status = models.ForeignKey('TestCaseRun', null=True, blank=True)
    
    description = models.TextField(blank=True)
    precondition = models.TextField(blank=True)
    
    name = models.CharField(max_length=512)

    def __unicode__(self):
        return self.name


class TestCaseStepRun(core.BaseModel):
    testcase = models.ForeignKey('TestCaseRun')
    description = models.TextField()
    expected = models.TextField(blank=True)
    sequence = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['sequence']


class TestCaseRunStatus(core.BaseModel):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=7, blank=True)
