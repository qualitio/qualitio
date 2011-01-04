from django.db import models
from qualitio.core import models as core


class Requirement(core.BaseDirectoryModel):
    description = models.TextField(blank=True)
    alias = models.CharField(blank=True, max_length=512) #TODO: alias is not unique and should be moved to core.models
    release_target = models.DateField(blank=True, null=True)
    dependencies = models.ManyToManyField("Requirement", related_name="blocks", null=True, blank=True)
    
    def get_absolute_url(self):
        return "/require/" % self.id
    
    def __unicode__(self):
        return "%s%s" % (self.path, self.name)
