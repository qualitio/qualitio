from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify

from qualitio.core.custommodel.models import CustomizableModel
from qualitio import THREAD


class Organization(CustomizableModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField('auth.User', through='OrganizationMember')

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
    organization = models.ForeignKey('Organization')
    user = models.ForeignKey('auth.User', related_name='organization_member')

    ADMIN = 0
    USER = 10
    USER_READONLY = 20
    INACTIVE = 999

    ROLE_CHOICES = (
        (ADMIN, u'Admin'),
        (USER, u'User'),
        (USER_READONLY, u'User - read only'),
        (INACTIVE, u'Inactive')
        )

    role = models.IntegerField(choices=ROLE_CHOICES, default=INACTIVE)


class ProjectManager(models.Manager):
    def get_query_set(self):
        organization = getattr(THREAD, 'organization', None)

        qs = super(ProjectManager, self).get_query_set()
        if organization:
            qs = qs.filter(organization=organization)

        return qs


class Project(CustomizableModel):
    default_name = "default"

    organization = models.ForeignKey('Organization')
    team = models.ManyToManyField('auth.User', related_name="projects", blank=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    homepage = models.URLField(verify_exists=False, blank=True)
    description = models.TextField(blank=True)

    modified_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = ProjectManager()

    class Meta:
        unique_together = ("organization", "name")

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
