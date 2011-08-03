from qualitio.report.views import *
from qualitio.core.middleware import THREAD


def get_absolute_url():
    project = getattr(THREAD, "project", None)
    if project:
        return "%s%s/" % (THREAD.project.get_absolute_url(),
                           "report")
    return "/report/"
