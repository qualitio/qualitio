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
    origin = models.ForeignKey("store.TestCase")
    status = models.ForeignKey("TestCaseRunStatus", default=1)

    class Meta(store.TestCaseBase.Meta):
        parent_class = 'TestRun'
        for_parent_unique = False

    @property
    def bugs_history(self):
        return Bug.objects.filter(testcaserun__origin=self.origin)\
            .exclude(alias__in=self.bugs.values_list('alias',flat=True))

    @classmethod
    # TODO: move this method to TestRun objects methods
    def run(cls, test_case, test_run):
        test_case_run = TestCaseRun.objects.create(name=test_case.name,
                                                   description=test_case.description,
                                                   precondition=test_case.precondition,
                                                   parent=test_run,
                                                   origin=test_case)

        for test_case_step in test_case.steps.all():
            test_case_run.steps.create(description=test_case_step.description,
                                       expected=test_case_step.expected,
                                       sequence=test_case_step.sequence)
        return test_case_run


class TestCaseStepRun(store.TestCaseStepBase):
    testcaserun = models.ForeignKey('TestCaseRun', related_name="steps")


class TestCaseRunStatus(core.BaseModel):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=7, blank=True)

    def __unicode__(self):
        return self.name


class Bug(core.BaseModel):
    testcaserun = models.ForeignKey('TestCaseRun', related_name="bugs")
    alias = models.CharField(max_length=512)
    url = models.URLField(blank=True, verify_exists=False)
    name = models.CharField(max_length=512, blank=True)
    status = models.CharField(max_length=128, blank=True)
    resolution = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = ("testcaserun", "alias")

    def __unicode__(self):
        return "#%s" % self.alias


