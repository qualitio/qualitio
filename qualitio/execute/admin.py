from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from qualitio.execute import models
from qualitio.core.admin import PathModelInline, DirectoryModelAdmin, PathModelAdmin

class TestRunInline(PathModelInline):
    model = models.TestRun


class TestRunDirectoryAdmin(DirectoryModelAdmin):
    inlines = [ TestRunInline ]
admin.site.register(models.TestRunDirectory, TestRunDirectoryAdmin)


class TestCaseRunInline(admin.TabularInline):
    model = models.TestCaseRun
    extra = 0


class TestRunAdmin(PathModelAdmin):
    inlines = [ TestCaseRunInline ]
admin.site.register(models.TestRun, TestRunAdmin)


class TestCaseRunStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color")
admin.site.register(models.TestCaseRunStatus, TestCaseRunStatusAdmin)
