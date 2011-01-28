from mptt.models import MPTTModel
from django.db import models


class BaseModel(models.Model):
    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True

    def clean(self):
        for name, value in filter(lambda x: not x[0].startswith("_"), self.__dict__.items()):
            if isinstance(value, basestring):
                setattr(self, name, getattr(self, name).strip())

    def __unicode__(self):
        return self.name


class BasePathModel(BaseModel):
    #TODO: move here parent, name fileds from BaseDiBaseDirectoryModel,
    #      or crate MetaClass wich will handle this situation
    path = models.CharField(max_length=2048, blank=True)
    name = models.CharField(max_length=1024)


    class Meta:
        abstract = True
        unique_together = (("name", "parent"),)

    def _get_path(self):
        #TODO: exception needed when class is improperly configured,
        #      when parent is not defined in orginal class
        if self.parent:
            return "%s%s/" % (self.parent.path,
                              self.parent.name)
        return "/"

    def save(self, *args, **kwargs): # TODO: a bit risky stuff
        self.path = self._get_path()
        super(BasePathModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s/%s" % (self.path, self.name)


class BaseDirectoryModel(MPTTModel, BasePathModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')


    class Meta:
        abstract = True
        unique_together = (("name", "parent"),)

    def save(self, *args, **kwargs):
        super(BaseDirectoryModel, self).save(*args, **kwargs)
        for child in self.children.all():
            child.save()
        # Children 2nd category ;)
        if hasattr(self, "subchildren"):
            for subchild in self.subchildren.all():
                subchild.save()

