from nose.tools import *
from qualitio.core.tests.utils import BaseTestCase

from qualitio.filter.tests.testapp.models import Directory, File, FileDescription
from qualitio.filter.filterset import ModelFilterSet


class FileFilterSet(ModelFilterSet):
    class Meta:
        model = File


REVERSE_RELATION_SELECT_CHOICES = {
    'Unknown': '1',
    'Yes': '2',
    'No': '3',
    }


class FilterSetTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['filter.tests.testapp'])

        self.root_dir = Directory.objects.create(name="root")
        self.test_file = File.objects.create(name="Test file", parent=self.root_dir)
        self.file_with_no_desc = File.objects.create(
            name="Test file with no description",
            parent=self.root_dir)
        self.file_desc = FileDescription.objects.create(title="Test file desc.",
                                                        file=self.test_file)

    def test_filter_adds_reverse_relation_filter_automatically(self):
        filterset = FileFilterSet()
        assert_true('filedescription' in filterset.filters)

    def test_filter_reverse_relation(self):
        filterset = FileFilterSet({'filedescription': REVERSE_RELATION_SELECT_CHOICES['Yes']})
        # filter should pass only those File objects which has any FileDescription's
        self.assertQuerysetEqual(filterset.qs, [self.test_file], lambda x: x)

    def test_exclude_those_with_no_reverse_relation(self):
        filterset = FileFilterSet({'filedescription': REVERSE_RELATION_SELECT_CHOICES['No']})
        # filter should pass only those File objects which hasn't got any FileDescription
        # with 'file' attribute setted up.
        self.assertQuerysetEqual(filterset.qs, [self.file_with_no_desc], lambda x: x)
