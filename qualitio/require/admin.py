from django.contrib import admin
from qualitio.require import models
from qualitio.core.admin import DirectoryModelAdmin
# from reversion.admin import VersionAdmin

class RequirementAdmin(DirectoryModelAdmin):
    readonly_fields = ('path',)
admin.site.register(models.Requirement, RequirementAdmin)
