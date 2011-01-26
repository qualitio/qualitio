from django.contrib import admin
from qualitio.requirements import models
from qualitio.core.admin import DirectoryModelAdmin

class RequirementAdmin(DirectoryModelAdmin):
    readonly_fields = ('path',)
admin.site.register(models.Requirement, RequirementAdmin)
