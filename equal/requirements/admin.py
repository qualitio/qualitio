from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from equal.requirements.models import Requirement

class RequirementAdmin(MPTTModelAdmin):
    list_display = ('name', 'modified_time', "created_time")
    readonly_fields = ('path',)
admin.site.register(Requirement, RequirementAdmin)
