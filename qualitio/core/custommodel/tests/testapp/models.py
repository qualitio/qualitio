from django.db import models

from qualitio.core.custommodel.models import ModelCustomization
from qualitio.require.models import Requirement


class RequirementCustomization(ModelCustomization):
    special_alias = models.IntegerField(null=True, blank=True)
    testfield = models.TextField(blank=True)

    class Meta:
        customization_target = Requirement
