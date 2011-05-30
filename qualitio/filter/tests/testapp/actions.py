from qualitio.filter import actions
from qualitio.filter.tests.testapp import models


class ChangeFileParent(actions.ChangeParent):
    model = models.File


class ChangeDirectoryParent(actions.ChangeParent):
    model = models.Directory
