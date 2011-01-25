from django.db import models
from qualitio.core import models as core


class Requirement(core.BaseDirectoryModel):
    dependencies = models.ManyToManyField("Requirement", related_name="blocks", null=True, blank=True)
    release_target = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return "/require/" % self.id
    
    def __unicode__(self):
        return "%s%s" % (self.path, self.name)
