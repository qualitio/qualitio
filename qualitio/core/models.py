from mptt.models import MPTTModel
from django.db import models
from django.core.exceptions import ImproperlyConfigured, ValidationError


class BaseModel(models.Model):
    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def clean(self):
        for name, value in filter(lambda x: not x[0].startswith("_"), self.__dict__.items()):
            if isinstance(value, basestring):
                setattr(self, name, getattr(self, name).strip())


class AbstractPathModel(BaseModel):
    """
    Abstract class that holds common tree-node attributes
    and validates node path uniquity.
    """
    path = models.CharField(max_length=2048, blank=True)
    name = models.CharField(max_length=1024)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s%s" % (self.path, self.name)

    def save(self, validate_path_unique=True, *args, **kwargs):
        if validate_path_unique:
            self.clean()
        super(AbstractPathModel, self).save(*args, **kwargs)

    def clean(self):
        qs = self.__class__._default_manager
        qs = qs.filter(parent=self.parent, name=self.name)

        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError('"parent" and "name" fields need to be always unique together.')


# TODO: those two classes below should go to separate module core.models.fields
#       following django conventions
class ReverseSingleRelatedObjectDescriptor(models.fields.related.ReverseSingleRelatedObjectDescriptor):
    def __set__(self, instance, value):
        super(ReverseSingleRelatedObjectDescriptor, self).__set__(instance, value)

        # syncronize the path attribute
        if hasattr(instance, 'parent_id') and instance.parent:
            instance.path = "%s%s/" % (instance.parent.path, instance.parent.name)
        else:
            instance.path = "/"


class PathSyncForeignKeyField(models.ForeignKey):
    # This method is re-written from
    # django.db.models.related.ForeignKey.contribute_to_class
    # It looks exactly the same as the method except it uses
    # our own ReverseSingleRelatedObjectDescriptor implementation
    def contribute_to_class(self, cls, name):
        super(PathSyncForeignKeyField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, ReverseSingleRelatedObjectDescriptor(self))
        if isinstance(self.rel.to, basestring):
            target = self.rel.to
        else:
            target = self.rel.to._meta.db_table
        cls._meta.duplicate_targets[self.column] = (target, "o2m")


class BasePathModelMetaclass(models.base.ModelBase):
    def __new__(cls, class_name, bases, attrs):
        Meta = attrs.get('Meta')

        is_abstract = hasattr(Meta, 'abstract') and Meta.abstract
        has_meta_parent_class = hasattr(Meta, 'parent_class')
        has_parent_attr = ('parent' in attrs) or any(hasattr(b, 'parent') for b in bases)

        # TODO: this code below causes error in nose test framework
        # if not is_abstract and not has_parent_attr and not has_meta_parent_class:
        #     msg =  'Meta for BasePathModel subclass %s(%s)' % (class_name, bases)
        #     msg += ' should provide "parent_class" param.'
        #     raise ImproperlyConfigured(msg)

        if has_meta_parent_class and not is_abstract:
            parent = PathSyncForeignKeyField(Meta.parent_class,
                                             null=True, blank=True,
                                             related_name='subchildren')
            attrs['parent'] = parent

            # Django raises error when Meta contains unexpected attributes
            # so we'll remove it
            del Meta.parent_class

        return super(BasePathModelMetaclass, cls).__new__(cls, class_name, bases, attrs)


class BasePathModel(AbstractPathModel):
    __metaclass__ = BasePathModelMetaclass

    class Meta:
        abstract = True


class BaseDirectoryModel(MPTTModel, AbstractPathModel):
    parent = PathSyncForeignKeyField('self', null=True, blank=True, related_name='children')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseDirectoryModel, self).save(*args, **kwargs)
        for child in self.children.all():
            child.save()
        # Children 2nd category ;)
        if hasattr(self, "subchildren"):
            for subchild in self.subchildren.all():
                subchild.save()
