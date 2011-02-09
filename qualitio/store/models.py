from django.db import models
from qualitio import core

class TestCaseBase(core.BasePathModel):
    requirement = models.ForeignKey('requirements.Requirement', null=True, blank=True)

    description = models.TextField(blank=True)
    precondition = models.TextField(blank=True)

    class Meta(core.BasePathModel.Meta):
        abstract = True


class TestCaseStepBase(core.BaseModel):
    description = models.TextField()
    expected = models.TextField(blank=True)
    sequence = models.PositiveIntegerField(null=True, default=0)

    class Meta:
        abstract = True


class TestCaseDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)


class TestCase(TestCaseBase):
    class Meta(TestCaseBase.Meta):
        parent_class = 'TestCaseDirectory'


class TestCaseStep(TestCaseStepBase):
    testcase = models.ForeignKey('TestCase')

    class Meta:
        ordering = ['sequence']


class Attachment(core.BaseModel):
    testcase = models.ForeignKey('TestCase')
    name = models.CharField(max_length=512)
    attachment = models.FileField(upload_to="attachments")
