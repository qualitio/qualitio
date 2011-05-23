from django.db import models
from qualitio import core


class TestCaseBaseManager(core.BaseManager):
    select_related_fields = core.BaseManager.select_related_fields + ['requirement']


class TestCaseBase(core.BasePathModel):
    requirement = models.ForeignKey('require.Requirement', null=True, blank=True)

    description = models.TextField(blank=True)
    precondition = models.TextField(blank=True)

    objects = TestCaseBaseManager()

    class Meta(core.BasePathModel.Meta):
        abstract = True


class TestCaseStepBase(core.BaseModel):
    description = models.TextField()
    expected = models.TextField(blank=True)
    sequence = models.PositiveIntegerField(null=True, default=0)

    class Meta(core.BaseModel.Meta):
        abstract = True
        ordering = ['sequence']
        verbose_name = "step"


class TestCaseDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestCase(TestCaseBase):
    class Meta(TestCaseBase.Meta):
        parent_class = 'TestCaseDirectory'


class TestCaseStep(TestCaseStepBase):
    testcase = models.ForeignKey('TestCase', related_name="steps")

    def __unicode__(self):
        return "%s" % (int(self.sequence) + 1)


class Attachment(core.BaseModel):
    testcase = models.ForeignKey('TestCase')
    name = models.CharField(max_length=512)
    attachment = models.FileField(upload_to="attachments")

