from django.db import models

from qualitio.core import ModelCustomization
from qualitio.core.tests.testapp.models import Directory


class DirectoryCustomization(ModelCustomization):
    special_alias = models.IntegerField(null=True, blank=True)
    testfield = models.TextField(blank=True)

    class Meta:
        model = Directory
