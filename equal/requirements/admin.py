from django.contrib import admin
# from treebeard.admin import TreeAdmin
# from django_mptt.admin import ModelAdmin
from mptt.admin import MPTTModelAdmin
from equal.requirements.models import Requirement

class DirectoryAdmin(MPTTModelAdmin):
    exclude = ("dependency_root",)
    list_display = ('name', 'modified_time', "created_time")
admin.site.register(Requirement, DirectoryAdmin)
