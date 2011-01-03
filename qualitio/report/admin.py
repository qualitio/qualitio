from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from qualitio.report.models import *

class QueryInline(admin.TabularInline):
    model = Query

class ReportAdmin(admin.ModelAdmin):
    inlines = [ QueryInline,]
    list_display = ("directory", "name")
    list_display_links = ('name',)

admin.site.register(Report, ReportAdmin)
admin.site.register(ReportDirectory, MPTTModelAdmin)
