import reversion
from qualitio.core.middleware import THREAD
from qualitio.require.models import Requirement

if not reversion.is_registered(Requirement):
    reversion.register(Requirement)


def get_absolute_url():
    project = getattr(THREAD, "project", None)
    if project:
        return "%s%s/" % (THREAD.project.get_absolute_url(),
                           "require")
    return "/require/"
