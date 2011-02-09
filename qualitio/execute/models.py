from django.db import models
from qualitio import core
from qualitio import store


class TestRunDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestRun(core.BasePathModel):
    notes = models.TextField(blank=True)

    class Meta(core.BasePathModel.Meta):
        parent_class = 'TestRunDirectory'


class TestCaseRun(store.TestCaseBase):
    status = models.ForeignKey("TestCaseRunStatus")
    bugs = models.ManyToManyField("Bug")

    class Meta(store.TestCaseBase.Meta):
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


class Bug(core.BaseModel):
    id = models.CharField(primary_key=True, max_length=512)
    url = models.URLField(blank=True, verify_exists=False)
    name = models.CharField(max_length=512, blank=True)
    status = models.CharField(max_length=128, blank=True)
    resolution = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return "#%s: %s" % (self.id, self.name)


