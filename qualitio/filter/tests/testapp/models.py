from django.db import models
from qualitio.core.tests.testapp.models import File, Directory


class FileDescription(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.ForeignKey(File, null=True)
    mode = models.CharField(max_length=3, choices=[
            ('r', 'read'),
            ('w', 'write'),
            ('w+', 'append'),
            ])
