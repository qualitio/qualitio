from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve

from qualitio.report.models import Report

def bound_reports(request):
    app_name = resolve(request.path).app_name
    bound_types = \
        ContentType.objects.exclude(report__bound_type__isnull=True).filter(app_label=app_name)

    reports = {}
    for bound_type in bound_types:
        reports[bound_type.model] = Report.objects.filter(bound_type=bound_type)

    return {'BOUND_VIEWS': reports}

