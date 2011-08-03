from django.contrib import admin
from qualitio.require import models
from qualitio import core


class RequirementAdmin(core.DirectoryModelAdmin):
    list_display = core.DirectoryModelAdmin.list_display + ["alias"]
admin.site.register(models.Requirement, RequirementAdmin)
