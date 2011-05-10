from __future__ import with_statement
from nose.tools import *
from operator import attrgetter

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from qualitio.core.tests.utils import BaseTestCase
from qualitio.core.tests.testapp.models import File, Directory

class BaseManagerTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['core.tests.testapp'])
        self.root = Directory.objects.create(name="root")

        # we need to create a lot of children
        for i in range(100):
            File.objects.create(name='file_%s' % i, parent=self.root)

    def test_only_one_query(self):
        # simulating getting attributes function
        get_attibutes = attrgetter('parent', 'name', 'path')

        with self.assertNumQueries(1):
            for file_obj in File.objects.all():
                get_attibutes(file_obj)
