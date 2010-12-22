from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from equal.store.models import *

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 0
    readonly_fields = ("path",)

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class TestCaseDirectoryAdmin(MPTTModelAdmin):
    inlines = [ TestCaseInline ]
    list_display = ("name",)
    list_display_links = ('name',)
    readonly_fields = ("path",)
admin.site.register(TestCaseDirectory, TestCaseDirectoryAdmin)

class TestCaseStepInline(admin.TabularInline):
    model = TestCaseStep
    extra = 1

class TestCaseAdmin(admin.ModelAdmin):
    inlines = [ TestCaseStepInline,
                AttachmentInline ]
    list_display = ("path", "name")
    readonly_fields = ("path",)
admin.site.register(TestCase, TestCaseAdmin)
