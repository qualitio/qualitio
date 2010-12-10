from mptt.models import MPTTModel
from django.db import models

class BaseModel(models.Model):
    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BasePathModel(BaseModel):
    path = models.CharField(max_length=2048, blank=True)
    
    class Meta:
        abstract = True

    def _get_path(self):
        if self.parent:
            return "%s%s/" % (self.parent.path,
                              self.parent.name)
        return "/"
        
    def save(self, *args, **kwargs): # TODO: a bit risky stuff
        self.path = self._get_path()
        super(BasePathModel, self).save(*args, **kwargs)
        if hasattr(self, "children"): #TODO: change abstration model
            for child in self.children.all(): # path update on children nodes 
                child.save() 


class BaseDirectoryModel(MPTTModel, BasePathModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=1024)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name
