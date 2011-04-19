from django.views import debug
from django.template import Template, TemplateSyntaxError
from django.core.exceptions import ValidationError


def get_template_exception_info(exception):
    origin, (start, end) = exception.source
    template_source = origin.reload()
    upto = line = 0
    for num, next in enumerate(debug.linebreak_iter(template_source)):
        if start >= upto and end <= next:
            line = num
        upto = next
    return line


def template_validate(template):
    try:
        Template(template)
    except TemplateSyntaxError as e:
        raise ValidationError({"template": "Line %s: %s"
                               % (get_template_exception_info(e), e)})

