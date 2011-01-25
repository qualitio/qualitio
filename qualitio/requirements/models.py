from django.db import models
from qualitio.core import models as core


class Requirement(core.BaseDirectoryModel):
    dependencies = models.ManyToManyField("Requirement", related_name="blocks", null=True, blank=True)
    #TODO: alias is not unique and should be moved to core.models
    alias = models.CharField(blank=True, max_length=512)
    release_target = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return "/require/" % self.id
    
    def __unicode__(self):
        return "%s%s" % (self.path, self.name)
