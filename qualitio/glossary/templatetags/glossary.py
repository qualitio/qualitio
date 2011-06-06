import re

from django import template
from django.utils.safestring import mark_safe
from qualitio.glossary.forms import WORD_RE
from qualitio.glossary.models import Word, Representation

register = template.Library()

@register.simple_tag(takes_context=True)
def glossary_aware(context, text):
    language = context['request'].session.get('glossary_language', None)

    def translate(m):
        word_html = '<span class="glosarry-word %s">%s</span>'
        try: 
            word = Word.objects.get(name=m.group(1))
            print word
            try:
                representation = word.representation_set.get(language=language)
                if representation.representation:
                    return mark_safe(word_html % ("translation", representation.representation))
                return mark_safe(word_html % ("no-translation", m.group(1)))
            except Representation.DoesNotExist:
                return mark_safe(word_html % ("no-translation", m.group(1)))
        except Word.DoesNotExist: 
            return mark_safe(word_html % ("no-word", m.group(1)))
    
    return re.sub("\$(%s)\$" % WORD_RE, translate, text)
