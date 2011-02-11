from django.contrib import admin
from qualitio import core
from qualitio.execute import models


class TestRunInline(core.PathModelInline):
    model = models.TestRun


class TestRunDirectoryAdmin(core.DirectoryModelAdmin):
    inlines = [ TestRunInline ]
admin.site.register(models.TestRunDirectory, TestRunDirectoryAdmin)


class TestCaseRunInline(admin.TabularInline):
    model = models.TestCaseRun
    extra = 0


class TestRunAdmin(core.PathModelAdmin):
    inlines = [ TestCaseRunInline ]
admin.site.register(models.TestRun, TestRunAdmin)


class TestCaseStepRunInline(admin.TabularInline):
    model = models.TestCaseStepRun
    extra = 0


class TestCaseRunAdmin(core.PathModelAdmin):
    list_display = core.PathModelAdmin.list_display + ("status",)
    inlines = [ TestCaseStepRunInline ]
admin.site.register(models.TestCaseRun, TestCaseRunAdmin)


class TestCaseRunStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color")
admin.site.register(models.TestCaseRunStatus, TestCaseRunStatusAdmin)


class BugAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "resolution", "url")
admin.site.register(models.Bug, BugAdmin)
