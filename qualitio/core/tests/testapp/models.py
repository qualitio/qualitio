# this module contains test-only models to test
# core abstract models functionality.
# In test env we'll simulate file system.
from qualitio.core.models import BasePathModel, BaseDirectoryModel


class File(BasePathModel):
    class Meta(BasePathModel.Meta):
        parent_class = 'Directory'


class Directory(BaseDirectoryModel):
    pass
