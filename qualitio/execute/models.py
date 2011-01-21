from django.db import models
from mptt.models import MPTTModel

### TODO: switch with models to BaseModels
class TestRunDirectory(MPTTModel):
    parent = models.ForeignKey('self', null=True, blank=True)

    name = models.CharField(max_length=512)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return "/execute/testrun/" % self.id

    def get_path(self):
        if self.get_ancestors():
            return "/%s/" % "/".join(map(lambda x: x.name, self.get_ancestors()))
        return "/"

    def __unicode__(self):
        return '%s%s' % (self.get_path(),self.name)


class TestRun(models.Model):
    parent = models.ForeignKey('TestRunDirectory')

    name = models.CharField(max_length=512)
    notes = models.TextField(blank=True)


class TestCaseRun(models.Model):
    parent = models.ForeignKey('TestRun', null=True, blank=True)
    requirement = models.ForeignKey('requirements.Requirement', null=True, blank=True)
    
    description = models.TextField(blank=True)
    precondition = models.TextField(blank=True)
    
    name = models.CharField(max_length=512)
        
    def __unicode__(self):
        return self.name

class TestCaseStep(core.BaseModel):
    testcase = models.ForeignKey('TestCase')
    description = models.TextField()
    expected = models.TextField(blank=True)
    sequence = models.PositiveIntegerField(null=True, default=0)
    
    class Meta:
        ordering = ['sequence']

class Status(models.Model):
    name = models.CharField(max_length=512)
    color = models.CharField(max_length=512, blank=True)
