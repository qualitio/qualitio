from nose.tools import *

from qualitio.core.tests.utils import BaseTestCase
from qualitio.core.tests.testapp.forms import DirectoryForm
from qualitio.core.tests.testapp.models import Directory


class MoveDirectoryFormTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['core.tests.testapp'])

        self.root = Directory.objects.create(parent=None,
                                             name="root")

        self.directory = Directory.objects.create(parent=self.root,
                                                  name="directory")


    def test_no_self_as_parent(self):
        directory_form = DirectoryForm(instance=self.directory)

        self.assertTrue(self.root in directory_form.fields['parent'].queryset)
        self.assertTrue(self.directory not in directory_form.fields['parent'].queryset)

    def test_no_descendants_to_choice(self):

        child1 = Directory.objects.create(parent=self.directory,
                                          name="Child1")

        child2 = Directory.objects.create(parent=self.directory,
                                          name="Child2")

        directory_form = DirectoryForm(instance=self.directory)

        print directory_form.fields['parent'].queryset
        self.assertTrue(child1 not in directory_form.fields['parent'].queryset)
        self.assertTrue(child2 not in directory_form.fields['parent'].queryset)
