import datetime

from qualitio.core.tests.utils import BaseTestCase
from qualitio.core.tests.testapp.models import Directory
from qualitio.core import CustomizableModelForm
from qualitio.core.custommodel.tests.testapp import models


TESTAPP_MODULE = 'qualitio.core.custommodel.tests.testapp'


# Look to qualitio.custommodel.tests.testapp.models module to see
# how to create model customizations
class CreatingModelCustomization(BaseTestCase):
    def setUp(self):
        self.addTestApps([TESTAPP_MODULE])

    def test_adds_custom_meta_attr_to_customizator_model(self):
        msg = "%s customizator should have '_custom_meta' attribute" % models.DirectoryCustomization
        assert hasattr(models.DirectoryCustomization, '_custom_meta'), msg

    def test_request_for_not_existed_customization_dont_saves_new_one(self):
        directory = Directory(name='Root')

        # no customizations at all
        self.assertEquals(models.DirectoryCustomization.objects.count(), 0)

        # new customization object is created BUT NOT SAVED
        customization = directory.customization

        # make sure 'customization' property cached object properly
        self.assertEquals(customization, directory._customization_cache)
        self.assertEquals(customization.origin, directory)


class CustomizableModelAPI(BaseTestCase):
    def setUp(self):
        self.addTestApps([TESTAPP_MODULE])

    def test_custom_values_returns_dict_with_fields_values(self):
        directory = Directory.objects.create(name="Root")
        directory.customization.special_alias = 12
        directory.customization.testfield = "Test content"
        directory.save()  # directory.customization.save also invoked

        values = directory.custom_values()

        self.assertTrue(isinstance(values, dict))
        self.assertEquals(len(values), 2)

        for key in ['special alias', 'testfield']:
            assert key in values, '"%s" key is not in %s' % (key, values)


class CreatingCustomizableModelWithForm(BaseTestCase):
    def setUp(self):
        self.addTestApps([TESTAPP_MODULE])

    def form_class(self, model, exclude=()):
        model_, exclude_= model, exclude
        class DirectoryForm(CustomizableModelForm):
            class Meta:
                model = model_
                exclude = exclude_
        return DirectoryForm

    def test_form_has_fields_from_model_customization_object(self):
        form_class = self.form_class(Directory)
        expected = set([
                'path', 'name', 'parent', # original
                'testfield', 'special_alias',  # field from DirectoryCustomization class
                ])
        current = set(form_class.base_fields.keys())
        self.assertEquals(expected, current)

    # TODO: there's still no support for 'fields' option
    def test_form_exclude_works_for_model_customization_as_well(self):
        form_class = self.form_class(Directory, exclude=(
                'path', 'name',  # exlude from Directory model
                'testfield',  # exclude from DirectoryCustomization model
                ))
        expected = set([
                'parent',  # original
                'special_alias',  # field from DirectoryCustomization class
                ])
        current = set(form_class.base_fields.keys())
        self.assertEquals(expected, current)

    def test_customizable_model_form_can_edit_model_customization_fields_as_well(self):
        directory = Directory.objects.create(name="Root", parent=None)
        form_class = self.form_class(Directory)

        # let's edit the object
        form = form_class({
                # editing directory
                'name': 'Root',

                # editing directory.customization
                'special_alias': '1',
                'testfield': 'Test field content',
                }, instance=directory)

        assert form.is_valid(), "Somethings wrong - this form should be valid! %s" % form.errors
        directory = form.save()

        self.assertEquals(directory.customization.special_alias, 1)
        self.assertEquals(directory.customization.testfield, 'Test field content')

    def test_customizable_model_form_can_create_model_customization_fields_as_well(self):
        form_class = self.form_class(Directory)

        # let's edit the object
        form = form_class({
                # editing directory
                'name': 'New root',
                'parent': None,

                # editing directory.customization
                'special_alias': '10',
                'testfield': 'Test field content 3',
                })

        assert form.is_valid(), "Somethings wrong - this form should be valid! %s" % form.errors
        directory = form.save()

        self.assertEquals(directory.customization.special_alias, 10)
        self.assertEquals(directory.customization.testfield, 'Test field content 3')
