from nose.tools import *

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from qualitio.core.tests.utils import BaseTestCase
from qualitio.core.tests.testapp.models import File, Directory


class BasePathModelSubclassTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['core.tests.testapp'])
        self.root_dir = Directory.objects.create(name="root")

    @raises(IntegrityError)
    def test_BasePath_based_object_save_exception_without_parent(self):
        File.objects.create(name="myFile")

    def test_BasePath_based_object_need_to_have_name_and_parent_to_save(self):
        try:
            test_file = File.objects.create(name="myFile", parent=self.root_dir)
        except ValidationError, e:
            self.fail("The exception shouldn't be raised here.")
