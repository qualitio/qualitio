from django.contrib import admin
from qualitio.require import models
from qualitio import core


class RequirementAdmin(core.DirectoryModelAdmin):
    list_display = core.DirectoryModelAdmin.list_display.insert(-2, "alias")
admin.site.register(models.Requirement, RequirementAdmin)
