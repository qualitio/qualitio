from django.db import models
from django.template.defaultfilters import linebreaksbr
from qualitio import core


class TestCaseBaseManager(core.BaseManager):
    select_related_fields = core.BaseManager.select_related_fields + ['requirement',
                                                                      'status']


class TestCaseBase(core.BasePathModel):
    requirement = models.ForeignKey('require.Requirement', null=True, blank=True)

    description = models.TextField(blank=True)
    precondition = models.TextField(blank=True)

    objects = TestCaseBaseManager()

    # TODO: remove this two, replace them with custom model fields
    def description_br(self):
        return linebreaksbr(self.description)

    def precondition_br(self):
        return linebreaksbr(self.precondition)

    class Meta(core.BasePathModel.Meta):
        abstract = True


class TestCaseStepBase(core.BaseModel):
    description = models.TextField()
    expected = models.TextField(blank=True)
    sequence = models.PositiveIntegerField(null=True, default=0)

    # TODO: remove this two, the same as TestCaseBase
    def description_br(self):
        return linebreaksbr(self.description)

    def expected_br(self):
        return linebreaksbr(self.expected)

    class Meta(core.BaseModel.Meta):
        abstract = True
        ordering = ['sequence']
        verbose_name = "step"


class TestCaseDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Directories'
        verbose_name= 'Directory'


class TestCaseStatus(core.BaseStatusModel):
    default_name = "Proposed"

    class Meta:
        verbose_name_plural = 'Test case statuses'
        verbose_name= 'Test case status'


class TestCase(TestCaseBase):
    status = models.ForeignKey('TestCaseStatus', default=TestCaseStatus.default)

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

