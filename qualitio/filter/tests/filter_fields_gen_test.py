from nose.tools import *
from qualitio.core.tests.utils import BaseTestCase

from qualitio.filter.tests.testapp.models import FileDescription
from qualitio.filter.fields import generate_field_forms


class FieldGeneration(BaseTestCase):
    def setUp(self):
        self.addTestApps(['filter.tests.testapp'])

    def assertHaveRequiredFields(self, FieldForm, expected=('q',)):
        fields = set(FieldForm.base_fields.keys())
        expected = set(expected)
        self.assertEquals(fields, expected)

    def test_foreign_key_field(self):
        FieldForm = generate_field_forms(FileDescription, fields=('file'))[0]
        self.assertHaveRequiredFields(FieldForm)

    def test_text_field(self):
        FieldForm = generate_field_forms(FileDescription, fields=('title',))[0]
        self.assertHaveRequiredFields(FieldForm, ['q', 'lookup'])

        FieldForm = generate_field_forms(FileDescription, fields=('mode',))[0]
        self.assertHaveRequiredFields(FieldForm)
