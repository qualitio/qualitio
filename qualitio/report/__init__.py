from qualitio.core.middleware import THREAD
from qualitio.report.views import report_external, report_bound

def get_absolute_url():
    project = getattr(THREAD, "project", None)
    if project:
        return "%s%s/" % (THREAD.project.get_absolute_url(),
                           "report")
    return "/report/"
