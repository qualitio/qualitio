from django.contrib import admin
from qualitio.glossary import models


class WordAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = ("id", "name", 'modified_time', "created_time")
admin.site.register(models.Word, WordAdmin)


class RepresentationAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = ("id", 'word', "language", "representation", "modified_time", "created_time")
admin.site.register(models.Representation, RepresentationAdmin)


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = ("id", "name", 'modified_time', "created_time")
admin.site.register(models.Language, LanguageAdmin)
