import reversion
from qualitio import module_absolute_url
from qualitio.execute.models import TestRunDirectory, TestRun, TestRunStatus, TestCaseRun, Bug, TestCaseRunStatus


if not reversion.is_registered(TestRun):
    reversion.register(TestRun, follow=["testcaserun_set"])
    reversion.register(TestCaseRun, follow=["parent", "bugs"])
    reversion.register(Bug, ["testcaserun"])

if not reversion.is_registered(TestRunDirectory):
    reversion.register(TestRunDirectory)


get_absolute_url = module_absolute_url(module_name="execute")
verbose_name = "execute"
