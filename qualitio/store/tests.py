import re

from nose.tools import *
from django.test import TestCase as DjangoTestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from qualitio.store.models import TestCase, TestCaseDirectory
from qualitio.store.forms import TestCaseDirectoryForm


class StoreModelParentFieldGenerationTest(DjangoTestCase):
    def test_TestCase_should_have_parent_field_defined(self):
        fields = dict((f.name, f) for f in TestCase._meta.fields)
        assert_true('parent' in fields)


class TestCaseDirectoryUniquityTest(DjangoTestCase):
    def setUp(self):
        self.big_project = TestCaseDirectory.objects.create(name="BigProject")

    def data_that_should_cause_an_error(self):
        return {
            'name': 'BigProject',
            'parent': None,
            }

    @raises(ValidationError)
    def test_directory_name_and_parent_should_be_unique_on_model_save(self):
        new_big_project = TestCaseDirectory(**self.data_that_should_cause_an_error())
        new_big_project.save()

    @raises(ValidationError)
    def test_directory_name_and_parent_should_be_unique_on_model_full_clean(self):
        new_big_project = TestCaseDirectory(**self.data_that_should_cause_an_error())
        new_big_project.full_clean()

    def test_directory_name_and_parent_should_be_unique_form(self):
        form = TestCaseDirectoryForm(self.data_that_should_cause_an_error())

        assert_true(form.is_bound)
        assert_false(form.is_valid())
        assert_equals(len(form.errors), 1)

    @raises(IntegrityError)
    def test_cannot_create_testcase_with_none_parent(self):
        TestCase.objects.create(name="Simple test 1")

    @raises(ValueError)
    def test_cannot_create_testcase_with_explicite_none_parent(self):
        TestCase.objects.create(name="Simple test 1", parent=None)

    def test_cannot_create_two_testcases_with_the_same_parent(self):
        TestCase.objects.create(name="Simple test 1", parent=self.big_project)
        try:
            TestCase.objects.create(name="Simple test 1", parent=self.big_project)
        except ValidationError, e:
            pass
        else:
            self.fail("The exception should be raised here.")

    def test_directory_name_and_parent_should_be_unique_view(self):
        result = self.client.post(
            '/store/ajax/testcasedirectory/new/valid/',
            self.data_that_should_cause_an_error())
        assert_true(re.search(r'"success": false', result.content))


class OrderingTreeTest(TestCase):
    def setUp(self):
        self.big_project = TestCaseDirectory.objects(name="BigProject")

        # testcases
        manager = TestCase.objects
        self.tc_z = manager.create(parent=self.big_project, name='z')
        self.tc_x = manager.create(parent=self.big_project, name='x')
        self.tc_a = manager.create(parent=self.big_project, name='b')

        # testcase directories
        manager = TestCaseDirectory.objects
        self.tcd_z = manager.create(parent=self.big_project, name='z')
        self.tcd_x = manager.create(parent=self.big_project, name='x')
        self.tcd_a = manager.create(parent=self.big_project, name='b')

    def test_subchildren_returned_in_alphabetical_order(self):
        children = list(self.big_project.subchildren.all())
        expected = [self.tc_a, self.tc_x, self.tc_z]
        assert_equals(expected, children)

    def test_children_returned_in_alphabetical_order(self):
        children = list(self.big_project.children.all())
        expected = [self.tcd_a, self.tcd_x, self.tcd_z]
        assert_equals(expected, children)
