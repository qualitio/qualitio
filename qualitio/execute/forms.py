from qualitio import core
from qualitio.execute import models


class TestRunDirectoryForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestRunDirectory


class TestRunForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestRun

