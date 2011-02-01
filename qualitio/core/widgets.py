from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class RawRadioSelectRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        return mark_safe(u'\n%s\n' % u'\n'.join([force_unicode(w) for w in self]))
