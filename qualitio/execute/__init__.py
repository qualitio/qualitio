import reversion
from qualitio.core.middleware import THREAD
from qualitio.execute.models import TestRunDirectory, TestRun, TestRunStatus, TestCaseRun, Bug, TestCaseRunStatus


if not reversion.is_registered(TestRun):
    reversion.register(TestRun, follow=["testcaserun_set"])
    reversion.register(TestCaseRun, follow=["parent", "bugs"])
    reversion.register(Bug, ["testcaserun"])

if not reversion.is_registered(TestRunDirectory):
    reversion.register(TestRunDirectory)


def get_absolute_url():
    project = getattr(THREAD, "project", None)
    if project:
        return "%s%s/" % (THREAD.project.get_absolute_url(),
                           "execute")
    return "/execute/"

verbose_name = "execute"
