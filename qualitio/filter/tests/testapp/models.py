from django.db import models
from qualitio.core.tests.testapp.models import File, Directory


class FileDescription(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.ForeignKey(File, null=True)
