from django.contrib import admin
from qualitio.projects.models import Project, Organization, OrganizationMember
from qualitio.core.utils import FieldList


class ProjectAdmin(admin.ModelAdmin):
    search_fields = FieldList(["id", "name"])
    list_display = FieldList(["id", "name", "organization", "homepage", "modified_time", "created_time"])
admin.site.register(Project, ProjectAdmin)


class OrganizationAdminInline(admin.TabularInline):
    model = OrganizationMember


class OrganizationAdmin(admin.ModelAdmin):
    search_fields = FieldList(["id", "name"])
    list_display = FieldList(["id", "name", "homepage", "googleapps_domain", "modified_time", "created_time"])
    inlines = [ OrganizationAdminInline ]
    readonly_fields = ("slug",)
admin.site.register(Organization, OrganizationAdmin)

