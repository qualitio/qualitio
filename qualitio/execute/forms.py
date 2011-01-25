from qualitio.core.forms import PathModelForm
from qualitio.execute import models


class TestRunDirectoryForm(PathModelForm):
    class Meta(PathModelForm.Meta):
        model = models.TestRunDirectory


class TestRunForm(PathModelForm):
    class Meta(PathModelForm.Meta):
        model = models.TestRun

