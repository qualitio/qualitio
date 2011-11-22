from django.contrib import admin
from qualitio.core.utils import FieldList

from qualitio.organizations.models import Project, Organization, OrganizationMember


class ProjectAdmin(admin.ModelAdmin):
    search_fields = FieldList(
        ["id", "name"]
    )
    list_display = FieldList(
        ["id", "name", "organization", "homepage",
         "modified_time", "created_time"]
    )
admin.site.register(Project, ProjectAdmin)


class OrganizationAdminInline(admin.TabularInline):
    model = OrganizationMember
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    search_fields = FieldList(
        ["id", "name"]
    )
    list_display = FieldList(
        ["id", "slug", "name", "googleapps_domain",
         "homepage", "modified_time", "created_time"]
    )
    inlines = [ OrganizationAdminInline ]
admin.site.register(Organization, OrganizationAdmin)

