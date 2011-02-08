from django.db import models
from qualitio import core
from qualitio import store


class TestRunDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestRun(core.BasePathModel):
    notes = models.TextField(blank=True)

    class Meta:
        parent_class = 'TestRunDirectory'


class TestCaseRun(store.TestCaseBase):
    status = models.ForeignKey('TestCaseRunStatus')

    class Meta:
        parent_class = 'TestRun'

    @staticmethod
    def run_testcase(testcase):
        pass


class TestCaseStepRun(store.TestCaseStepBase):
    testcaserun = models.ForeignKey('TestCaseRun')

    class Meta:
        ordering = ['sequence']


class TestCaseRunStatus(core.BaseModel):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=7, blank=True)

    def __unicode__(self):
        return self.name
