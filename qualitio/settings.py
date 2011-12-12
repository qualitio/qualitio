import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin Qualitio', 'admin@qualitio.com'),
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
    'qualitio.organizations.middleware.OrganizationMiddleware',
    'qualitio.organizations.middleware.ProjectMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'qualitio.core.middleware.LoginRequiredMiddleware',
    'qualitio.core.middleware.QueriesCounterMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'qualitio.urls'

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = '/login/'

LOGIN_EXEMPT_URLS = (
    (r'^$', lambda request: request.organization is None),
    r'^r/.*',
    r'^none/$',
    r'^static/',
    r'^login/',
    r'^inactive/',
    r'^admin/',
    r'^register/.*',
    r'^associate/*',
    r'^complete/*',
    r'^project/(?P<slug>[\w-]+)/report/external/*',
    r'^__debug__/.*',
    r'^api/.*',
    r'^googleapps_setup/$',
    r'^google_checkout/$',
    r'^paypal_ipn/$',
    )

PROJECT_EXEMPT_URLS = (
    r'^static/.*',
    r'^admin/.*',
    r'^login/.*',
    r'^register/.*',
    r'^associate/*',
    r'^complete/*',
    r'^__debug__/.*',
    r'^api/.*',
    r'^project/new/.*',
    )

ORGANIZATION_EXEMPT_URLS = (
    r'^static/',
    r'^admin/',
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
    'south',
    'pagination',
    'compressor',
    'dbtemplates',
    'tastypie',
    'articles',
    'django_extensions',

    'qualitio.core.custommodel',  # iternal core django application
    'qualitio.core',
    'qualitio.organizations',
    'qualitio.require',
    'qualitio.report',
    'qualitio.execute',
    'qualitio.store',
    'qualitio.filter',
    'qualitio.actions',
    'qualitio.glossary',
    'qualitio.payments',
    'qualitio.chart',

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
                               "qualitio.core.context_processors.core",
                               "qualitio.core.context_processors.module",
                               "qualitio.organizations.context_processors.main")

AUTH_PROFILE_MODULE = 'organizations.UserProfile'

SOCIAL_AUTH_IMPORT_BACKENDS = (
    'qualitio.googleapps.backends',
)

AUTHENTICATION_BACKENDS = (
    'qualitio.googleapps.backends.GoogleBackend',
    'qualitio.googleapps.backends.GoogleAppsBackend',
    'qualitio.organizations.auth.backends.OrganizationModelBackend',
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
DBTEMPLATES_USE_REVERSION = True
DBTEMPLATES_MEDIA_PREFIX = MEDIA_URL
DBTEMPLATES_USE_CODEMIRROR = False
DBTEMPLATES_AUTO_POPULATE_CONTENT = False


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'notifications@qualitio.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = "Qualitio Notifications <notifications@qualitio.com>"

try:
    from local_settings import *
except ImportError:
    pass
