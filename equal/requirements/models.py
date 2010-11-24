from django.db import models
# from treebeard.mp_tree import MP_Node
from mptt.models import MPTTModel

class BaseModel(models.Model):
    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    

class DirectoryBaseModel(MPTTModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=1024)
    
    class Meta:
        abstract = True

    # Will generate extra SQL for every request to database, 
    # could be huge pain in the ass in list views
    def get_path(self):
        if self.get_ancestors():
            return "/%s/" % "/".join(map(lambda x: x.name, self.get_ancestors()))
        return "/"
    

class Requirement(DirectoryBaseModel, BaseModel):
    description = models.TextField(blank=True)

    def __unicode__(self):
        return 'Requirement: %s' % self.name

    def get_absolute_url(self):
        return "/require/" % self.id

