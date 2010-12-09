from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from equal.requirements.models import Requirement, RequirementDependency

class RequirementAdmin(MPTTModelAdmin):
    list_display = ('name', 'modified_time', "created_time")
    readonly_fields = ('path',)
admin.site.register(Requirement, RequirementAdmin)

class RequirementDependencyAdmin(MPTTModelAdmin):
    list_display = ('__unicode__', 'modified_time', "created_time")
    readonly_fields = ('path',)
admin.site.register(RequirementDependency, RequirementDependencyAdmin)
