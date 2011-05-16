from django.db import models

from qualitio import core
from qualitio import store


class TestRunDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestRun(core.BasePathModel):
    notes = models.TextField(blank=True)

    @property
    def passrate(self):
        pass

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

class TestCaseRun(store.TestCaseBase):
    origin = models.ForeignKey("store.TestCase")
    status = models.ForeignKey("TestCaseRunStatus", default=1)

    class Meta(store.TestCaseBase.Meta):
        parent_class = 'TestRun'
        for_parent_unique = False
        parent_class_relation = "testcases"
        unique_together = ("parent", "origin")

    @property
    def bugs_history(self):
        return Bug.objects.filter(testcaserun__origin=self.origin)\
            .exclude(alias__in=self.bugs.values_list('alias',flat=True))

    def save(self, *args, **kwargs):
        super(TestCaseRun, self).save(*args, **kwargs)


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


