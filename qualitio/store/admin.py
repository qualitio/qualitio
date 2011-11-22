from django.contrib import admin
from qualitio.store import models
from qualitio import core


class TestCaseInline(core.PathModelInline):
    model = models.TestCase


class TestCaseDirectoryAdmin(core.DirectoryModelAdmin):
    inlines = [ TestCaseInline ]
admin.site.register(models.TestCaseDirectory, TestCaseDirectoryAdmin)


class TestCaseStepInline(admin.TabularInline):
    model = models.TestCaseStep
    extra = 1



class TestCaseAdmin(core.PathModelAdmin):
    inlines = [ TestCaseStepInline ]
admin.site.register(models.TestCase, TestCaseAdmin)


class TestCaseStatus(core.BaseModelAdmin):
    list_display = core.BaseModelAdmin.list_display.insert(2, "name")
admin.site.register(models.TestCaseStatus, TestCaseStatus)
