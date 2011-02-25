from nose.tools import *

from django.http import QueryDict

from qualitio.core.tests.utils import BaseTestCase
from qualitio.store.models import TestCase as StoreTestCase
from qualitio.filter.fields import generate_field_forms
from qualitio.filter.filter import Filter


# params construction:
# group_id - form_class_id - form_id - field_name


class BuildingFormsFromParamsTest(BaseTestCase):
    def setUp(self):
        self.default_exclude = ('lft', 'rght', 'tree_id', 'level')
        self.form_classes = generate_field_forms(StoreTestCase, exclude=self.default_exclude)

    def get_number_of_forms(self, filter):
        number_of_forms = 0
        for g in filter.groups.values():
            number_of_forms += len(g.forms)
        return number_of_forms

    def assertFilterGroupConsistency(self, params, expected_number_of_groups=-1, expected_number_of_forms=-1):
        filter = Filter(params, form_classes=self.form_classes)
        filter.build_from_params()
        number_of_forms = self.get_number_of_forms(filter)
        self.assertEquals(expected_number_of_groups, len(filter.groups))
        self.assertEquals(expected_number_of_forms, number_of_forms)

    def test_should_have_proper_number_of_forms(self):
        params = QueryDict('&'.join([
                    '1-0-1-to_date=',
                    '1-0-1-from_date=',
                    '1-1-1-to_date=',
                    '1-1-1-from_date=',
                    '1-4-1-q=',

                    '2-4-1-q=3',

                    '3-4-1-q=',
                    ]))
        self.assertFilterGroupConsistency(params, expected_number_of_groups=3, expected_number_of_forms=5)

    def test_problematic(self):
        params = QueryDict('&'.join([
                    '1-0-1-from_date=',
                    '1-0-1-to_date=',
                    '1-1-1-from_date=',
                    '1-1-1-to_date=',
                    '1-4-1-q=1',

                    '2-4-1-q=3',

                    '3-4-1-q=',

                    '4-4-1-q=',

                    '5-1-1-from_date=',
                    '5-1-1-to_date=',
                    ]))
        self.assertFilterGroupConsistency(params, expected_number_of_groups=5, expected_number_of_forms=7)
