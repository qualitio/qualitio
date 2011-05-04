from nose.tools import *
from qualitio.core.tests.utils import BaseTestCase

from qualitio.filter.tests.testapp.models import FileDescription
from qualitio import filter as filterapp


class FilterFieldsGeneration(BaseTestCase):
    def setUp(self):
        self.addTestApps(['filter.tests.testapp'])

    def create_filter_class(self, model=None, fields=None, exclude=()):
        _Meta = None
        _model, _fields, _exclude = model, fields, exclude

        if _model:
            class _Meta:
                model = _model
                fields = _fields
                exclude = _exclude

        class Filter(filterapp.ModelFilter):
            Meta = _Meta

        return Filter

    def assertHaveRequiredFieldFilters(self, FilterClass, expected=()):
        fields = set(FilterClass.base_filters.keys())
        expected = set(expected)
        self.assertEquals(fields, expected)

    def test_field_filters_generation(self):
        Filter = self.create_filter_class(model=FileDescription)
        self.assertHaveRequiredFieldFilters(Filter, expected=('file', 'title', 'mode'))

    def test_setting_field_option(self):
        Filter = self.create_filter_class(model=FileDescription, fields=('file', 'title'))
        self.assertHaveRequiredFieldFilters(Filter, expected=('file', 'title'))

    def test_setting_exclude_option(self):
        Filter = self.create_filter_class(model=FileDescription, exclude=('file', 'title'))
        self.assertHaveRequiredFieldFilters(Filter, expected=('mode',))
