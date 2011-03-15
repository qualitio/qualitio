import reversion

from models import TestRunDirectory, TestRun, TestCaseRun, Bug


if not reversion.is_registered(TestRun):
    reversion.register(TestRun, follow=["testcaserun_set"])
    reversion.register(TestCaseRun, follow=["parent", "bugs"])
    reversion.register(Bug, ["testcaserun"])


if not reversion.is_registered(TestRunDirectory):
    reversion.register(TestRunDirectory)
