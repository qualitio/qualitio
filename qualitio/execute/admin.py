from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from qualitio.execute.models import *

class TestRunInline(admin.TabularInline):
    model = TestRun
    readonly_fields = ("path",)


class TestRunDirectoryAdmin(MPTTModelAdmin):
    inlines = [ TestRunInline ]
    list_display = ("id", "parent", "name")
    list_display_links = ("id", "name")
    readonly_fields = ("path",)
admin.site.register(TestRunDirectory, TestRunDirectoryAdmin)

class TestCaseRunInline(admin.TabularInline):
    model = TestCaseRun
    extra = 0

class TestRunAdmin(admin.ModelAdmin):
    list_display = ("id", "path", "name")
    list_display_links = ("id", "name")
    inlines = [ TestCaseRunInline ]
    readonly_fields = ("path",)
admin.site.register(TestRun, TestRunAdmin)

class TestCaseRunStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color")
admin.site.register(TestCaseRunStatus, TestCaseRunStatusAdmin)
