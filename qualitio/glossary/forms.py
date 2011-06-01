from django import forms
from qualitio import core
from qualitio.glossary import models


class WordForm(core.BaseModelForm):
    name = forms.RegexField(regex=r"^[a-zA-Z0-9_\-]+$",
                            error_messages={"invalid": 'Invalid character used. Allowed characters are: "a-zA-Z0-9_-"'})
    class Meta(core.BaseModelForm.Meta):
        model = models.Word


class RepresentationForm(core.BaseModelForm):
    class Meta(core.BaseModelForm.Meta):
        model = models.Representation
        fields = ("representation",)


class RepresentationFormsSet(object):
    def __init__(self, data=None, word=None):
        self.forms = []
        if word and data:
            for representation in word.representation_set.all():
                self.forms.append((representation.language,
                                  RepresentationForm(data,
                                                     instance=representation,
                                                     prefix=representation.language.name)))
        elif word and not data:
            for representation in word.representation_set.all():
                self.forms.append((representation.language,
                                   RepresentationForm(instance=representation,
                                                      prefix=representation.language.name)))
        elif not word and data:
            for language in models.Language.objects.all():
                self.forms.append((language,
                                   RepresentationForm(data,
                                                      prefix=language.name)))
        else:
            for language in models.Language.objects.all():
                self.forms.append((language,
                                   RepresentationForm(prefix=language.name)))

    def is_valid(self):
        return not any([ not form.is_valid() for language, form in self.forms])

    def __iter__(self):
        for language, form  in self.forms:
            yield language, form

