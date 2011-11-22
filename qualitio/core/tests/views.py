from nose.tools import *

from django.test.client import Client
from django.utils import simplejson as json
from qualitio.core.tests.utils import BaseTestCase
from qualitio.core.tests.testapp.models import File, Directory
from django.contrib.auth.models import User

class ViewTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['core.tests.testapp'])

        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        self.client = Client()
        self.client.login(username='john', password='johnpassword')


    def test_direcotry_root(self):
        obj = Directory.objects.create(name="level_1")

        response = self.client.get('/testapp/ajax/get_ancestors',
                                   {'type': obj._meta.module_name, 'id': obj.pk})
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["target"], "%s_%s" % (obj.pk, obj._meta.module_name))

    def test_file_flat(self):
        directory = Directory.objects.create(name="level_1")
        obj = File.objects.create(name="file",parent=directory)

        response = self.client.get('/testapp/ajax/get_ancestors',
                                    {'type': obj._meta.module_name, 'id': obj.pk})

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["target"], "%s_%s" % (obj.pk, obj._meta.module_name))


    def test_file_deep(self):
        directory1 = Directory.objects.create(name="level_1")
        directory2 = Directory.objects.create(name="level_2", parent=directory1)
        directory3 = Directory.objects.create(name="level_2", parent=directory2)
        obj = File.objects.create(name="file",parent=directory3)

        response = self.client.get('/testapp/ajax/get_ancestors',
                                    {'type': obj._meta.module_name, 'id': obj.pk})

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["target"], "%s_%s" % (obj.pk, obj._meta.module_name))

