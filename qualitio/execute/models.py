from django.db import models
from django.conf import settings

from qualitio import core
from qualitio import store
from qualitio import glossary

import mangers


class TestRunDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Test run directories'


class TestRunStatus(core.BaseStatusModel):
    pass


class TestRun(core.BasePathModel):
    notes = models.TextField(blank=True)
    passrate = models.FloatField(default=0)
    translation = models.ForeignKey("glossary.Language", default=glossary.Language.default)
    status = models.ForeignKey("TestRunStatus", default=TestRunStatus.default)

    class Meta(core.BasePathModel.Meta):
        parent_class = 'TestRunDirectory'

    def testcase_setup(self, test_cases):

        to_create = []
        for test_case in test_cases:
            if test_case.id not in self.testcases.values_list("origin__id" ,flat=True):
                to_create.append(test_case)
                self.run(test_case)

        to_delete_ids = set(self.testcases.values_list("origin__id", flat=True))\
            - set(test_cases.values_list("id", flat=True))

        self.testcases.filter(origin__id__in=to_delete_ids).delete()

        to_delete = store.TestCase.objects.filter(id__in=to_delete_ids)

        return to_create, to_delete

    def run(self, test_case):
        test_case_run = self.testcases.create(name=test_case.name,
                                              description=test_case.description,
                                              precondition=test_case.precondition,
                                              origin=test_case)

        for test_case_step in test_case.steps.all():
            test_case_run.steps.create(description=test_case_step.description,
                                       expected=test_case_step.expected,
                                       sequence=test_case_step.sequence)

        return test_case_run


    def update_passrate(self):
        self.passrate = self.testcases.passrate()
        self.save(force_update=True)

    def copy(self):
        testrun_copy = super(TestRun, self).copy()

        for testcase in store.TestCase.objects.filter(testcaserun__parent=self):
            testrun_copy.run(testcase)

        return testrun_copy

    @property
    def bugs(self):
        return Bug.objects.filter(testcaserun__parent=self)\
            .values("name","alias")\
            .annotate(count=models.Count("alias"))


class TestCaseRunStatus(core.BaseStatusModel):
    default_name = "IDLE"

    color = models.CharField(max_length=7, blank=True)
    total = models.BooleanField(
        help_text="Count test cases with this status to total in test run passrate?")
    passed = models.BooleanField(
        help_text="Count test cases with this status to passed test cases in test run passrate?")

    class Meta:
        verbose_name_plural = 'Test case run statuses'

    def __init__(self, *args, **kwargs):
        super(TestCaseRunStatus, self).__init__(*args, **kwargs)
        self._orginals = {"total": self.total,
                          "passed": self.passed}

    def save(self, *args, **kwargs):
        if (self.total != self._orginals.get("total") or (self.passed != self._orginals.get("passed"))):
            for testrun in TestRun.objects.all():
                testrun.update_passrate()

        super(TestCaseRunStatus, self).save(*args, **kwargs)


class TestCaseRun(store.TestCaseBase):
    origin = models.ForeignKey("store.TestCase")
    status = models.ForeignKey("TestCaseRunStatus", default=TestCaseRunStatus.default)

    objects = mangers.TestCaseRunManager()

    class Meta(store.TestCaseBase.Meta):
        parent_class = 'TestRun'
        for_parent_unique = False
        parent_class_relation = "testcases"
        unique_together = ("parent", "origin")

    def __init__(self, *args, **kwargs):
        super(TestCaseRun, self).__init__(*args, **kwargs)
        self._orginals = {"status": self.status}

    @property
    def bugs_history(self):
        return Bug.objects.filter(testcaserun__origin=self.origin)\
            .filter(testcaserun__parent__id__lt=self.parent.id)

    def save(self, *args, **kwargs):
        super(TestCaseRun, self).save(*args, **kwargs)
        if self._orginals.get("status") != self.status:
            self.parent.update_passrate()


class TestCaseStepRun(store.TestCaseStepBase):
    testcaserun = models.ForeignKey('TestCaseRun', related_name="steps")


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

    def get_absolute_url(self):
        url = getattr(settings, "ISSUE_BACKEND_ABSOLUTE_URL", None)
        if url:
            return url % self.alias
        return "#"
