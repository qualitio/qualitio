from django.db import models

from django.template.defaultfilters import slugify
from qualitio.core.custommodel.models import CustomizableModel
from django.core.exceptions import ImproperlyConfigured


class Project(CustomizableModel):
    default_name = "default"

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def default(cls):
        try:
            return cls.objects.all()[0]
        except IndexError:
            raise ImproperlyConfigured("There is no default project, create one")

    def get_absolute_url(self):
        return '/project/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
