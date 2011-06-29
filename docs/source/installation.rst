Qualitio Project
================

Setup Development Environment (Debian/Ubuntu)
---------------------------------------------

In a case of using Debian sudo package is required. Some required
python packages are installed outside pypi repository but straight
from development repos so you may need also:
 - hg(mercurial)
 - git

On Debian-like systems simply type:
::

   sudo apt-get install mercurial git git-core


1. Clone this repository
::

   git clone git://github.com/qualitio/qualitio.git

2. Download and install fabric
::

   sudo apt-get install fabric or(not recommended),
   sudo easy_install -U fabric or,
   sudo pip install fabric.

3. Run development setup script
::

   python fabfile.py setup_development

4. Qualitio development environment is ready to use, lunch development server
::

   cd qualitio
   python manage.py runserver


Setup Remote Production Environment (Debian/Ubuntu)
---------------------------------------------------

In a case of using Debian sudo package is required. In some cases also
mercurial(hg) could be required.

1. Git clone this repository
::
   git clone git://github.com/qualitio/qualitio.git

2. Download and install fabric
::

   sudo easy_install -U fabric

If you don't have easy_install currently installed in your system
you can find it in python-setuptools package

3. Go to cloned project directory, and run deployment script
::

   cd qualtio
   fab setup_production fab setup_production -H _{HOST}_

_{HOST}_ is address of your target machine, if you had plan deploy
project locally simply type there _localhost_ (ssh server is required)


Updating Remote Production Environment (Debian/Ubuntu)
-------------------------------------------------

1. Go to cloned project directory, and run deployment script
::

   cd qualtio
   fab update_production -H _{HOST}_

_{HOST}_ is address of your target machine, if you had plan deploy
 project locally simply type there _localhost_ (ssh server is required).


Running Selenium Tests
----------------------

Before starting any testing you have to make sure that Java-jre is
installed (Selenium-RC test server is written used JAVA as running
platform).

1. Go to tests directory and start the Selenium-RC
::

   cd tests
   java -jar selenium-server.jar

2. Run test suite
::

   python tests.py

Check python tests.py for more available options
