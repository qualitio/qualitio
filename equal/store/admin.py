from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from equal.store.models import *

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 0

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class TestCaseDirectoryAdmin(admin.ModelAdmin):
    inlines = [ TestCaseInline ]
    list_display = ("parent", "name")
    list_display_links = ('name',)
admin.site.register(TestCaseDirectory, TestCaseDirectoryAdmin)

class TestCaseStepInline(admin.TabularInline):
    model = TestCaseStep
    extra = 1

class TestCaseAdmin(admin.ModelAdmin):
    inlines = [ TestCaseStepInline,
                AttachmentInline ]
admin.site.register(TestCase, TestCaseAdmin)

