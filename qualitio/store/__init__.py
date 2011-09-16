import reversion
from qualitio import module_absolute_url
from qualitio.store.models import (TestCaseBase, TestCaseStepBase, TestCase,
                                   TestCaseStep, TestCaseDirectory, TestCaseStatus)


if not reversion.is_registered(TestCase):
    reversion.register(TestCaseStep)
    reversion.register(TestCase, follow=["steps"])

if not reversion.is_registered(TestCaseDirectory):
    reversion.register(TestCaseDirectory)


get_absolute_url = module_absolute_url(module_name="store")
verbose_name = "store"
