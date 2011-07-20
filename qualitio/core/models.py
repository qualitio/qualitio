from copy import deepcopy
import re

from mptt.models import MPTTModel
from django.db import models
from django.core.exceptions import ImproperlyConfigured, ValidationError

from qualitio.core.custommodel.models import CustomizableModel


class BaseModel(CustomizableModel):
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
        return "%s: %s%s" % (self.pk, self.path, self.name)


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


class BaseManager(models.Manager):
    select_related_fields = ['parent']

    def get_query_set(self):
        return super(BaseManager, self).get_query_set().select_related(*self.select_related_fields)


class BasePathModel(AbstractPathModel):
    __metaclass__ = BasePathModelMetaclass

    objects = BaseManager()

    class Meta(AbstractPathModel.Meta):
        abstract = True

    def copy(self):
        copy_object = deepcopy(self)
        copy_object.id = None

        copy_exists = self.__class__.objects.filter(name__regex=r'%s \(copy\)$' % re.escape(self.name),
                                                    parent=self.parent).exists()
        if copy_exists:
            other_copies = self.__class__.objects.filter(name__regex=r'%s \(copy\s\d+?\)$' % re.escape(self.name),
                                                         parent=self.parent).order_by("name")

            copy_object.name = "%s (copy %s)" % (self.name, other_copies.count()+1)
            for i, copy in enumerate(other_copies,1):
                match = re.match("(.+)\s(\(copy(\s\d+)?\))", copy.name)
                copy_part = match.groups()[1]
                if copy_part != "(copy %s)" % i:
                    copy_object.name = "%s (copy %s)" % (self.name, i)
                    break
        else:
            copy_object.name = "%s (copy)" % self.name

        copy_object.save()
        return copy_object


class BaseDirectoryModel(MPTTModel, AbstractPathModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    objects = BaseManager()

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


class BaseStatusModel(BaseModel):
    default_name = "default"

    name = models.CharField(unique=True, max_length=255)

    class Meta(BaseModel.Meta):
        abstract = True

    @classmethod
    def default(cls):
        try:
            return cls.objects.all()[0]
        except IndexError:
            return cls.objects.create(name=cls.default_name)

    def __unicode__(self):
        return self.name
