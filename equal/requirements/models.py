from django.db import models
from equal.core import models as core


class Requirement(core.DirectoryBaseModel):
    description = models.TextField(blank=True)
    release_target = models.DateField()
    
    def __unicode__(self):
        return 'Requirement: %s' % self.name

    def get_absolute_url(self):
        return "/require/" % self.id
    
    def save(self, *args, **kwargs):
        super(Requirement, self).save(*args, **kwargs)
        RequirementDependency.objects.get_or_create(root=self)


class RequirementDependency(core.DirectoryBaseModel):
    root = models.OneToOneField('Requirement')
