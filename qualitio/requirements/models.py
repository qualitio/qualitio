from django.db import models
from qualitio import core


class Requirement(core.BaseDirectoryModel):
    dependencies = models.ManyToManyField("Requirement", related_name="blocks", null=True, blank=True)
    release_target = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
