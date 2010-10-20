from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from equal.execute.models import *

class TestRunInline(admin.TabularInline):
    model = TestRun

class TestRunDirectoryAdmin(admin.ModelAdmin):
    inlines = [ TestRunInline ]
    list_display = ("parent", "name")
    list_display_links = ('name',)
admin.site.register(TestRunDirectory, TestRunDirectoryAdmin)

admin.site.register(TestRun)
admin.site.register(TestCaseRun)
