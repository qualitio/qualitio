from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from qualitio.core.utils import FieldList


class BaseModelAdmin(admin.ModelAdmin):
    search_fields = FieldList(["id", "project"])
    list_display = FieldList(["id", "project", "modified_time", "created_time"])
    list_display_links = FieldList(["id"])


class PathModelAdmin(BaseModelAdmin):
    search_fields = BaseModelAdmin.search_fields.extend(["path", "name"])
    list_display = BaseModelAdmin.list_display.insert(2, "path", "name")
    list_display_links = BaseModelAdmin.list_display_links.append("name")
    readonly_fields = ["path"]


class DirectoryModelAdmin(MPTTModelAdmin, PathModelAdmin):
    pass


class PathModelInline(admin.TabularInline):
    readonly_fields = ["path"]
    extra = 0
