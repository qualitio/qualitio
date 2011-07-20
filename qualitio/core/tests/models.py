from nose.tools import *

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from qualitio.core.tests.utils import BaseTestCase
from qualitio.core.tests.testapp.models import File, Directory, FileNotUnique

class FileTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['core.tests.testapp'])
        self.root = Directory.objects.create(name="root")

    def test_create(self):
        file = File.objects.create(name="name", parent=self.root)
        self.assertTrue(file.pk is not None)

    @raises(IntegrityError)
    def test_create_without_parent(self):
        File.objects.create(name="name");

    @raises(ValidationError)
    def test_unique(self):
        File.objects.create(parent=self.root, name="name")
        File.objects.create(parent=self.root, name="name")

    def test_create_not_unique(self):
        FileNotUnique.objects.create(parent=self.root, name="name")
        FileNotUnique.objects.create(parent=self.root, name="name")

        self.assertEqual(FileNotUnique.objects.filter(parent=self.root).count(), 2)

    def test_related_name(self):
        File.objects.create(parent=self.root, name="name")
        FileNotUnique.objects.create(parent=self.root, name="name")

        self.assertEqual(self.root.unique_files.count(), 1)
        self.assertEqual(self.root.not_unique_files.count(), 1)


class FileCopyTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['core.tests.testapp'])
        self.root = Directory.objects.create(name="root")
        self.file = File.objects.create(name="file",
                                            parent=self.root)

    def test_copy(self):
        self.file_copy = self.file.copy()

        self.assertTrue(self.file_copy.name.startswith(self.file.name))
        self.assertTrue(self.file_copy.name.endswith("(copy)"))

        self.file_copy = self.file.copy()
        self.assertTrue(self.file_copy.name.startswith(self.file.name))
        self.assertTrue(self.file_copy.name.endswith("(copy 1)"))

        self.file_copy = self.file.copy()
        self.assertTrue(self.file_copy.name.startswith(self.file.name))
        self.assertTrue(self.file_copy.name.endswith("(copy 2)"))

        self.file_copy = self.file.copy()
        self.assertTrue(self.file_copy.name.startswith(self.file.name))
        self.assertTrue(self.file_copy.name.endswith("(copy 3)"))

    def test_remove_copy(self):
        file_copy = self.file.copy()
        file_copy_1 = self.file.copy()
        file_copy_2 = self.file.copy()

        file_copy_1.delete()

        again_file_copy_1 = self.file.copy()

        self.assertTrue(file_copy.name.endswith("(copy)"))
        self.assertTrue(again_file_copy_1.name.endswith("(copy 1)"))
        self.assertTrue(file_copy_2.name.endswith("(copy 2)"))

    def test_copy_from_copy(self):
        file_copy = self.file.copy()

        self.assertTrue(file_copy.name.startswith(self.file.name))
        self.assertTrue(file_copy.name.endswith("(copy)"))

        file_copy_copy = file_copy.copy()
        self.assertTrue(file_copy_copy.name.startswith(self.file.name))
        self.assertTrue(file_copy_copy.name.endswith("(copy) (copy)"))

        file_copy = self.file.copy()
        self.assertTrue(file_copy.name.startswith(self.file.name))
        self.assertTrue(file_copy.name.endswith("(copy 1)"))

