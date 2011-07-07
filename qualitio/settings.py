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
        'NAME': os.path.join(PROJECT_PATH, 'data.sqlite'),
    }
}

TIME_ZONE = 'Europe/Warsaw'

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True

DATE_FORMAT = "d-m-Y"
DATETIME_FORMAT = "d-m-Y, H:i:s"
DATE_INPUT_FORMATS = ('%d-%m-%Y',)

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

MEDIA_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static_admin/'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'dbtemplates.loader.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'qualitio.core.middleware.LoginRequiredMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'qualitio.urls'

LOGIN_REDIRECT_URL = "/account/"
LOGIN_URL = '/login/'

LOGIN_EXEMPT_URLS = (
    r'^static/',
    r'^login/.*',
    r'^register/.*',
    r'^associate/*',
    r'^complete/*',
    r'^report/external/*',
    r'^__debug__/.*',
    r'^api/.*',
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
    'django.contrib.markup',
    'django.contrib.humanize',

    'mptt',
    'social_auth',
    'django_nose',
    'reversion',
    'registration',
    'south',
    'pagination',
    'compressor',
    'dbtemplates',
    'tastypie',
    'articles',
    'django_extensions',

    'qualitio.core',
    'qualitio.core.custommodel',  # iternal core django application
    'qualitio.require',
    'qualitio.report',
    'qualitio.projects',
    'qualitio.execute',
    'qualitio.store',
    'qualitio.filter',
    'qualitio.glossary',

    'qualitio.customizations',
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


MPTT_ADMIN_LEVEL_INDENT = 30

ISSUE_BACKEND = "qualitio.execute.backends.bugzilla"
ISSUE_BACKEND_ABSOLUTE_URL = "https://bugzilla.mozilla.org/show_bug.cgi?id=%s"
ISSUE_BACKEND_BUGZILLA_URL = "https://bugzilla.mozilla.org/"



SOUTH_TESTS_MIGRATE = False


COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',
                        'compressor.filters.cssmin.CSSMinFilter']

COMPRESS = False

DBTEMPLATES_CACHE_BACKEND = 'dummy://127.0.0.1/'

try:
    from local_settings import *
except ImportError:
    pass
