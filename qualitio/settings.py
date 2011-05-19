import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'data/data.sqlite'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

DATE_FORMAT = "%y-%m-%d"
DATETIME_FORMAT = "m-d-Y, H:i:s"
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static_admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+xo!&_63g8h5(q0k$@+^lm@#a%l#3@1x(dw$c#e8p9jfx^*z*i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'qualitio.core.middleware.LoginRequiredMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'qualitio.urls'

LOGIN_REDIRECT_URL = "/require/"
LOGIN_URL = '/login/'

LOGIN_EXEMPT_URLS = (
    r'^static/',
    r'^login/.*',
    r'^register/.*',
    r'^associate/*',
    r'^complete/*',
    r'^report/external/*',
    r'^__debug__/.*',
    )

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.webdesign',

    'mptt',
    'debug_toolbar',
    'social_auth',
    'django_nose',
    'reversion',
    'registration',
    'south',
    'pagination',

    'qualitio.core',
    'qualitio.require',
    'qualitio.report',
    'qualitio.projects',
    'qualitio.execute',
    'qualitio.store',
    'qualitio.filter',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.request",
                               "django.contrib.messages.context_processors.messages",
                               "qualitio.core.context_processors.settings",
                               "qualitio.core.context_processors.development",
                               "qualitio.core.context_processors.core")

AUTH_PROFILE_MODULE = 'projects.UserProfile'


AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
)


INTERNAL_IPS = (
    '127.0.0.1',
    )

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

MPTT_ADMIN_LEVEL_INDENT = 30
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ISSUE_BACKEND = "qualitio.execute.backends.bugs.Bugzilla"
ISSUE_BACKEND_BUGZILLA_URL = "https://bugzilla.mozilla.org/"


SOUTH_TESTS_MIGRATE = False

try:
    from local_settings import *
except ImportError:
    pass

