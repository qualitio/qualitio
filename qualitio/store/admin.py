from django.contrib import admin
from qualitio.store import models
from qualitio.core.admin import PathModelInline, DirectoryModelAdmin, PathModelAdmin


class TestCaseInline(PathModelInline):
    model = models.TestCase


class TestCaseDirectoryAdmin(DirectoryModelAdmin):
    inlines = [ TestCaseInline ]
admin.site.register(models.TestCaseDirectory, TestCaseDirectoryAdmin)


class TestCaseStepInline(admin.TabularInline):
    model = models.TestCaseStep
    extra = 1


class AttachmentInline(admin.TabularInline):
    model = models.Attachment
    extra = 1


class TestCaseAdmin(PathModelAdmin):
    inlines = [ TestCaseStepInline,
                AttachmentInline ]
admin.site.register(models.TestCase, TestCaseAdmin)

