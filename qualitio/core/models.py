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
        ordering = ['name']

    def _get_path(self):
        if self.parent_id:
            return "%s%s/" % (self.parent.path, self.parent.name)
        return "/"

    def save(self, validate_path_unique=True, *args, **kwargs):
        self.path = self._get_path()
        if validate_path_unique:
            self.clean()
        super(AbstractPathModel, self).save(*args, **kwargs)

    def clean(self):
        if getattr(self, "_for_parent_unique", True):
            parent = self.parent if self.parent_id else None

            manager = self.__class__.objects
            qs = manager.filter(name=self.name, parent=parent)

            if self.pk:  # we do not want to search for *this* object
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError('"parent" and "name" fields need to be always unique together.')

    def __unicode__(self):
        return "%s%s" % (self.path, self.name)


class BasePathModelMetaclass(models.base.ModelBase):
    def __new__(cls, class_name, bases, attrs):
        Meta = attrs.get('Meta')

        is_abstract = hasattr(Meta, 'abstract') and Meta.abstract

        # TODO: this code below causes error in nose test framework
        # has_parent_attr = ('parent' in attrs) or any(hasattr(b, 'parent') for b in bases)
        # if not is_abstract and not has_parent_attr and not has_meta_parent_class:
        #     msg =  'Meta for BasePathModel subclass %s(%s)' % (class_name, bases)
        #     msg += ' should provide "parent_class" param.'
        #     raise ImproperlyConfigured(msg)

        if not is_abstract:
            if hasattr(Meta, 'parent_class'):
                related_name = 'subchildren'
                if hasattr(Meta, 'parent_class_relation'):
                    related_name = getattr(Meta, 'parent_class_relation')
                    del Meta.parent_class_relation
                parent = models.ForeignKey(Meta.parent_class, related_name=related_name)
                attrs['parent'] = parent
                del Meta.parent_class # Django raises error when Meta contains unexpected attributes

            if hasattr(Meta, 'for_parent_unique'):
                attrs['_for_parent_unique'] = getattr(Meta, 'for_parent_unique', False)
                del Meta.for_parent_unique

        return super(BasePathModelMetaclass, cls).__new__(cls, class_name, bases, attrs)


class BasePathModel(AbstractPathModel):
    __metaclass__ = BasePathModelMetaclass

    class Meta(AbstractPathModel.Meta):
        abstract = True


class BaseDirectoryModel(MPTTModel, AbstractPathModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    class Meta(AbstractPathModel.Meta):
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseDirectoryModel, self).save(*args, **kwargs)
        for child in self.children.all():
            child.save()
        # Children 2nd category ;)
        if hasattr(self, "subchildren"):
            for subchild in self.subchildren.all():
                subchild.save()
