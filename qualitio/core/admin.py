from django.contrib import admin
from mptt.admin import MPTTModelAdmin


class BaseModelAdmin(admin.ModelAdmin):
    search_fields = ["id", "project"]
    list_display = ["id", "project", "modified_time", "created_time"]
    list_display_links = ["id"]


class PathModelAdmin(BaseModelAdmin):
    search_fields = BaseModelAdmin.search_fields + ["path", "name"]
    list_display = ["id", "project", "path", "name", "modified_time", "created_time"]
    list_display_links = BaseModelAdmin.list_display_links + ["name"]
    readonly_fields = ["path"]


class DirectoryModelAdmin(MPTTModelAdmin, PathModelAdmin):
    pass


class PathModelInline(admin.TabularInline):
    readonly_fields = ["path"]
    extra = 0
