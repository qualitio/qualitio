from django.contrib import admin
from qualitio import core
from qualitio.glossary import models


class WordAdmin(core.BaseModelAdmin):
    list_display = core.BaseModelAdmin.list_display.insert(2, 'name')
admin.site.register(models.Word, WordAdmin)


class RepresentationAdmin(core.BaseModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", 'project', 'word', "language", "representation", "modified_time", "created_time"]
admin.site.register(models.Representation, RepresentationAdmin)


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", 'project', "name", 'modified_time', "created_time"]
admin.site.register(models.Language, LanguageAdmin)
