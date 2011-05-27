import re

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class RawRadioSelectRenderer(forms.widgets.RadioFieldRenderer):
    def _switch_tags(self, html):
        marks = re.search("(?P<label_begin><label.*?>)(?P<input><input.*?>)(?P<status>.*)(?P<label_end><.label>)",html).groupdict()

        return "%s%s%s%s" % (marks['label_begin'],
                             marks['status'],
                             marks['label_end'],
                             marks['input'])

    def render(self):
        return mark_safe(u'\n%s\n' % u'\n'.join([self._switch_tags(force_unicode(w)) for w in self]))

