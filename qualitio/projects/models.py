from django.db import models
# from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from qualitio.core.custommodel.models import CustomizableModel


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
            return cls.objects.create(name=cls.default_name)

    def get_absolute_url(self):
        return '/project/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
