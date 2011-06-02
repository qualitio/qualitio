from django.views.generic.simple import direct_to_template

from qualitio.core.utils import json_response, success, failed

from qualitio.glossary.models import Word
from qualitio.glossary.forms import WordForm, RepresentationFormsSet


def index(request):
    return direct_to_template(request, 'glossary/base.html')


def list(request):
    return direct_to_template(request, 'glossary/list.html', {"words_list": Word.objects.all()})


def new(request):
    word_form = WordForm()
    return direct_to_template(request, 'glossary/edit.html',
                              {"word_form": word_form,
                               "representation_form_list": RepresentationFormsSet()})


def edit(request, word_id=0):
    word = Word.objects.get(pk=word_id)
    word_form = WordForm(instance=word)
    return direct_to_template(request, 'glossary/edit.html',
                              {"word_form": word_form,
                               "representation_form_list": RepresentationFormsSet(word=word)})

@json_response
def edit_valid(request, word_id=0):
    if word_id:
        word = Word.objects.get(pk=word_id)
        word_form = WordForm(request.POST, instance=word)
        representation_form_list = RepresentationFormsSet(request.POST, word=word)

    else:
        word_form = WordForm(request.POST)
        representation_form_list = RepresentationFormsSet(request.POST)

    if word_form.is_valid() and representation_form_list.is_valid():
        word = word_form.save()
        for language, representation_form in representation_form_list:
            representation = representation_form.save(commit=False)
            representation.word = word
            representation.language = language
            representation.save()

        return success(message='Word saved',
                       data={"id": word.pk,
                             "name": word.name})

    else:
        return failed(message="Validation errors: %s" % word_form.error_message(),
                      data=word_form.errors_list())

