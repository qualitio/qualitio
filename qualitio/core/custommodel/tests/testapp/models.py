from django.db import models
from django.core.exceptions import ValidationError

from qualitio.core import ModelCustomization
from qualitio.core.tests.testapp.models import Directory


class DirectoryCustomization(ModelCustomization):
    special_alias = models.IntegerField(null=True, blank=True)
    testfield = models.TextField(blank=True)

    class Meta:
        model = Directory

    def clean_origin(self):
        if self.special_alias >= 100:
            raise ValidationError('Special alias hava to be < 100')
