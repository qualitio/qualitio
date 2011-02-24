# this module contains test-only models to test
# core abstract models functionality.
# In test env we'll simulate file system.
from qualitio.core.models import BasePathModel, BaseDirectoryModel


class Directory(BaseDirectoryModel):
    pass


class File(BasePathModel):
    class Meta(BasePathModel.Meta):
        parent_class = 'Directory'
        parent_class_relation = 'unique_files'


class FileNotUnique(BasePathModel):
    class Meta(BasePathModel.Meta):
        parent_class = 'Directory'
        parent_class_relation = 'not_unique_files'
        for_parent_unique = False
