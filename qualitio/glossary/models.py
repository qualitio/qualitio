from django.db import models
from qualitio import core


class Word(core.BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Language(core.BaseStatusModel):
    # ToDo: not to ideal base name, check implementation

    def save(self, *kwargs, **args):
        if self.id:
            super(Language, self).save(*kwargs, **args)
        else:
            super(Language, self).save(*kwargs, **args)
            for word in Word.objects.all():
                Representation.objects.get_or_create(language=self, word=word)


class Representation(core.BaseModel):
    word = models.ForeignKey('Word')
    language = models.ForeignKey('Language')
    representation = models.CharField(max_length=512, blank=True)

    class Meta(core.BaseModel.Meta):
        unique_together = ("word", "language")

    def __unicode__(self):
        return self.representation

