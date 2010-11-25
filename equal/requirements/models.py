from django.db import models

from mptt.models import MPTTModel

class BaseModel(models.Model):
    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    

class DirectoryBaseModel(MPTTModel, BaseModel):
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
    

class Requirement(DirectoryBaseModel):
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return 'Requirement: %s' % self.name

    def get_absolute_url(self):
        return "/require/" % self.id
    
    def save(self, *args, **kwargs):
        super(Requirement, self).save(*args, **kwargs)
        RequirementDependency.objects.get_or_create(root=self)


class RequirementDependency(DirectoryBaseModel):
    root = models.OneToOneField('Requirement')
