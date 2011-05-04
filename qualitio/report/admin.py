from django.contrib import admin
from qualitio import core
from qualitio.report import models


class ReportDirectoryAdmin(core.DirectoryModelAdmin):
    pass
admin.site.register(models.ReportDirectory, ReportDirectoryAdmin)

class ContextElement(admin.TabularInline):
    model = models.ContextElement

class ReportAdmin(core.PathModelAdmin):
    inlines = [ContextElement]
admin.site.register(models.Report, ReportAdmin)
