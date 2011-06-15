import reversion

from models import TestCaseBase, TestCaseStepBase, TestCase, TestCaseStep, TestCaseDirectory, TestCaseStatus


if not reversion.is_registered(TestCase):
    reversion.register(TestCaseStep)
    reversion.register(TestCase, follow=["steps"])


if not reversion.is_registered(TestCaseDirectory):
    reversion.register(TestCaseDirectory)
