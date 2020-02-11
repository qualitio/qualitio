from setuptools import setup, find_packages

VERSION = open("VERSION").read().strip("\n")


install_requires = [
    'Django==1.11.28',
    'Pygments==1.4',
    'South==0.7.3',
    'django-compressor==0.9.1',
    'django-debug-toolbar==0.8.5',
    'django-extensions==0.6',
    'django-filter==0.5.3',
    'django-nose==0.1.3',
    'django-reversion==1.4',
    'django-social-auth==0.3.15',
    'django-tables==0.2',
    'httplib2==0.6.0',
    'ipython==0.10.2',
    'networkx==1.4',
    'nose==1.0.0',
    'oauth2==1.5.170',
    'python-openid==2.2.5',
    'wsgiref==0.1.2',
    'django-pagination==1.0.7',
    'django-dbtemplates==1.0.1',
    'django-tastypie==0.9.9',

    'django_mptt',
    'django-registration',

    'distribute',
    'sphinx==1.0.7',
]


setup(name='qualitio',
      url = "http://qualitio.com",
      version=VERSION,
      packages=find_packages(),
      install_requires=install_requires,
      dependency_links = [
        "https://github.com/django-mptt/django-mptt/tarball/master",
        "https://bitbucket.org/ubernostrum/django-registration/get/58eef8330b0f.tar.gz"
        ],
      include_package_data = True,
      entry_points = {
        'console_scripts': [
            'qualitio-manage = qualitio.manage:manage_global',
            ],
        }
      )

