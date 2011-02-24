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
