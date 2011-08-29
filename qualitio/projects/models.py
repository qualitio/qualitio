from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify

from qualitio.core.custommodel.models import CustomizableModel


class Organization(CustomizableModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    description = models.TextField(blank=True)

    googleapps_domain = models.CharField(max_length=255, blank=True)

    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def setup(self, owner):
        pass

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Organization, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class OrganizationMember(CustomizableModel):
    organization = models.ForeignKey('Organization', related_name='members')
    user = models.ForeignKey('auth.User', related_name='organization')

    ROLE_CHOICES = (
        (u'admin', u'Admin'),
        (u'edit', u'User'),
        (u'read', u'User - read only'),
    )
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default="read")


class Project(CustomizableModel):
    default_name = "default"

    organization = models.ForeignKey('Organization')
    team = models.ManyToManyField('auth.User', related_name="projects", blank=True)

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    description = models.TextField(blank=True)

    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/project/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def setup(self):
        from qualitio.require.models import Requirement
        from qualitio.store.models import TestCaseDirectory, TestCaseStatus
        from qualitio.execute.models import TestRunDirectory, TestRunStatus, TestCaseRunStatus
        from qualitio.report.models import ReportDirectory
        from qualitio.glossary.models import Language

        # require
        Requirement.objects.create(name=self.name, project=self)

        # store
        TestCaseStatus.objects.create(name=TestCaseStatus.default_name, project=self)
        TestCaseDirectory.objects.create(name=self.name, project=self)

        # glossary
        Language.objects.create(name=Language.default_name, project=self)

        # execute
        TestRunStatus.objects.create(name=TestRunStatus.default_name, project=self)
        TestCaseRunStatus.objects.create(name=TestCaseRunStatus.default_name, project=self)
        TestRunDirectory.objects.create(name=self.name, project=self)

        # report
        ReportDirectory.objects.create(name=self.name, project=self)

    def __unicode__(self):
        return self.name
