from django.contrib import admin
from mptt.admin import MPTTModelAdmin


class PathModelAdmin(admin.ModelAdmin):
    list_display = ("path", "name")
    list_display_links = ('name',)
    readonly_fields = ("path",)


class DirectoryModelAdmin(MPTTModelAdmin, PathModelAdmin):
    pass


class PathModelInline(admin.TabularInline):
    readonly_fields = ("path",)
    extra = 0

