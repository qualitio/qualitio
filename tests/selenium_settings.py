import os
import sys

from settings import *

TEST_PATH =os.path.join(os.path.dirname(__file__), "../tests")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TEST_PATH, 'selenium-test-data.sqlite'),
    }
}
