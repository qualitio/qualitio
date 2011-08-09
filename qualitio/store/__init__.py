import reversion
from qualitio.core.middleware import THREAD
from qualitio.store.models import TestCaseBase, TestCaseStepBase, TestCase, TestCaseStep, TestCaseDirectory, TestCaseStatus


if not reversion.is_registered(TestCase):
    reversion.register(TestCaseStep)
    reversion.register(TestCase, follow=["steps"])

if not reversion.is_registered(TestCaseDirectory):
    reversion.register(TestCaseDirectory)


def get_absolute_url():
    project = getattr(THREAD, "project", None)
    if project:
        return "%s%s/" % (THREAD.project.get_absolute_url(),
                           "store")
    return "/store/"

verbose_name = "store"
