from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from qualitio.execute.models import *

class TestRunInline(admin.TabularInline):
    model = TestRun

class TestRunDirectoryAdmin(MPTTModelAdmin):
    inlines = [ TestRunInline ]
    list_display = ("id", "parent", "name")
    list_display_links = ("id", "name")
admin.site.register(TestRunDirectory, TestRunDirectoryAdmin)

admin.site.register(TestRun)
admin.site.register(TestCaseRun)
