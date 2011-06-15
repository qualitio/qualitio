from django import template
from qualitio.core import utils
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def load_dbtemplate(name):
    template_loader = utils.load_dbtemplate(name)()
    if template_loader:
        return mark_safe(template_loader.content)
    return ""
