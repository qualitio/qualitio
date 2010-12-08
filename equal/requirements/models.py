from django.db import models
from equal.core import models as core


class Requirement(core.BaseDirectoryModel):
    description = models.TextField(blank=True)
    release_target = models.DateField()
    
    def add_dependency(self, requirement):
        pass
    
    def get_absolute_url(self):
        return "/require/" % self.id
    
    def save(self, *args, **kwargs):
        super(Requirement, self).save(*args, **kwargs)
        RequirementDependency.objects.get_or_create(dependencyroot=self)
    
    def __unicode__(self):
        return "%s%s" % (self.path, self.name)

class RequirementDependency(core.BaseDirectoryModel):
    dependencyroot = models.OneToOneField('Requirement', related_name="dependencyroot")
