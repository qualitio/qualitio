from django import template
from qualitio.report.models import Report
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.inclusion_tag('report/bound_reports_menu.html', takes_context=True)
def bound_reports_menu(context, obj, current_view):

    content_type =  ContentType.objects.get_for_model(obj)
    reports = Report.objects.filter(bound_type=content_type)

    return {"reports": reports,
            "current_view": current_view,
            "model_name": content_type.model,
            "obj": obj}

