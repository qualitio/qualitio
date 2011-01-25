from django.contrib import admin
from mptt.admin import MPTTModelAdmin


class PathModelAdmin(admin.ModelAdmin):
    search_fields = ["id", "path", "name"]
    list_display = ("id", "path", "name", 'modified_time', "created_time")
    list_display_links = ("id", "name")
    readonly_fields = ("path",)


class DirectoryModelAdmin(MPTTModelAdmin, PathModelAdmin):
    pass


class PathModelInline(admin.TabularInline):
    readonly_fields = ("path",)
    extra = 0

