from qualitio import core
from qualitio.core.tests.testapp import models


class DirectoryForm(core.DirectoryModelForm):
    class Meta(core.DirectoryModelForm.Meta):
        model = models.Directory
