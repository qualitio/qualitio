import datetime

from qualitio.core.tests.utils import BaseTestCase
from qualitio.require.models import Requirement
from qualitio.core.custommodel.forms import CustomizableModelForm
from qualitio.core.custommodel.tests.testapp import models


TESTAPP_MODULE = 'qualitio.core.custommodel.tests.testapp'


# Look to qualitio.custommodel.tests.testapp.models module to see
# how to create model customizations
class CreatingModelCustomization(BaseTestCase):
    def setUp(self):
        self.addTestApps([TESTAPP_MODULE])

    def test_adds_custom_meta_attr_to_customizator_model(self):
        msg = "%s customizator should have '_custom_meta' attribute" % models.RequirementCustomization
        assert hasattr(models.RequirementCustomization, '_custom_meta'), msg

    def test_request_for_not_existed_customization_dont_saves_new_one(self):
        requirement = Requirement(name='Root')

        # no customizations at all
        self.assertEquals(models.RequirementCustomization.objects.count(), 0)

        # new customization object is created BUT NOT SAVED
        customization = requirement.customization

        # make sure 'customization' property cached object properly
        self.assertEquals(customization, requirement._customization_cache)
        self.assertEquals(customization.origin, requirement)


class CustomizableModelAPI(BaseTestCase):
    def setUp(self):
        self.addTestApps([TESTAPP_MODULE])

    def test_custom_fields_returns_dict_with_fields_values(self):
        requirement = Requirement.objects.create(name="Root")
        requirement.customization.special_alias = 12
        requirement.customization.testfield = "Test content"
        requirement.save()  # requirement.customization.save also invoked

        values = requirement.custom_fields()

        self.assertTrue(isinstance(values, dict))
        self.assertEquals(len(values), 2)

        for key in ['special alias', 'testfield']:
            assert key in values, '"%s" key is not in %s' % (key, values)


class CreatingCustomizableModelWithForm(BaseTestCase):
    def setUp(self):
        self.addTestApps([TESTAPP_MODULE])

    def form_class(self, model, exclude=()):
        model_, exclude_= model, exclude
        class RequirementForm(CustomizableModelForm):
            class Meta:
                model = model_
                exclude = exclude_
        return RequirementForm

    def test_form_has_fields_from_model_customization_object(self):
        form_class = self.form_class(Requirement)
        expected = set([
                'path', 'name', 'parent', 'dependencies', 'release_target', 'description', 'alias',  # original
                'testfield', 'special_alias',  # field from RequirementCustomization class
                ])
        current = set(form_class.base_fields.keys())
        self.assertEquals(expected, current)

    # TODO: there's still no support for 'fields' option
    def test_form_exclude_works_for_model_customization_as_well(self):
        form_class = self.form_class(Requirement, exclude=(
                'path', 'name', 'parent',  # exlude from Requirement model
                'testfield',  # exclude from RequirementCustomization model
                ))
        expected = set([
                'dependencies', 'release_target', 'description', 'alias',  # original
                'special_alias',  # field from RequirementCustomization class
                ])
        current = set(form_class.base_fields.keys())
        self.assertEquals(expected, current)

    def test_customizable_model_form_can_edit_model_customization_fields_as_well(self):
        requirement = Requirement.objects.create(name="Root", parent=None)
        form_class = self.form_class(Requirement)

        # let's edit the object
        form = form_class({
                # editing requirement
                'name': 'Root',
                'release_target': '12-06-2011',  # watchout for the date format!

                # editing requirement.customization
                'special_alias': '1',
                'testfield': 'Test field content',
                }, instance=requirement)

        assert form.is_valid(), "Somethings wrong - this form should be valid! %s" % form.errors
        requirement = form.save()

        self.assertEquals(requirement.release_target, datetime.date(2011, 6, 12))
        self.assertEquals(requirement.customization.special_alias, 1)
        self.assertEquals(requirement.customization.testfield, 'Test field content')

    def test_customizable_model_form_can_create_model_customization_fields_as_well(self):
        form_class = self.form_class(Requirement)

        # let's edit the object
        form = form_class({
                # editing requirement
                'name': 'New root',
                'release_target': '12-06-2011',  # watchout for the date format!
                'parent': None,

                # editing requirement.customization
                'special_alias': '10',
                'testfield': 'Test field content 3',
                })

        assert form.is_valid(), "Somethings wrong - this form should be valid! %s" % form.errors
        requirement = form.save()

        self.assertEquals(requirement.release_target, datetime.date(2011, 6, 12))
        self.assertEquals(requirement.customization.special_alias, 10)
        self.assertEquals(requirement.customization.testfield, 'Test field content 3')
