from django.db import models
from equal.requirements import models as core

class TestCaseDirectory(core.DirectoryBaseModel):
    pass

class TestCase(core.BaseModel):
    parent = models.ForeignKey('TestCaseDirectory', null=True, blank=True)
    requirement = models.ForeignKey('requirements.Requirement', null=True, blank=True)

    name = models.CharField(max_length=512)
    precondition = models.TextField(blank=True)

    def get_path(self):
        return "%s%s/" % (self.parent.get_path(),
                         self.parent.name)


class TestCaseStep(models.Model):
    testcase = models.ForeignKey('TestCase')
    description = models.TextField()
    expected = models.TextField()
    

class Attachment(core.BaseModel):
    testcase = models.ForeignKey('TestCase')
    name = models.CharField(max_length=512)
    attachment = models.FileField(upload_to="attachments")
