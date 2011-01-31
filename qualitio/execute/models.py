from django.db import models
from qualitio import core
from qualitio import store


class TestRunDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestRun(core.BasePathModel):
    parent = models.ForeignKey('TestRunDirectory', related_name="subchildren")

    notes = models.TextField(blank=True)


class TestCaseRun(store.TestCaseBase):
    parent = models.ForeignKey('TestRun', null=True, blank=True, related_name="subchildren")
    status = models.ForeignKey('TestCaseRun', null=True, blank=True)


class TestCaseStepRun(store.TestCaseStepBase):
    testcaserun = models.ForeignKey('TestCaseRun')

    class Meta:
        ordering = ['sequence']


class TestCaseRunStatus(core.BaseModel):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=7, blank=True)
