Qualitio Project
================

1. Setup Development Environment (Debian/Ubuntu): 
-------------------------------------------------

In a case of using Debian sudo package is required. Some required
python packages are installed outside pypi repository but straight
from development repos so you may need also: hg(mercurial), sudo apt-get install mercurial,git, sudo apt-get install git-core
   

1. Git clone this repository:
   * git clone git://github.com/qualitio/qualitio.git 

1. Download and install fabric:
   * sudo apt-get install fabric or(not recommended),
   * sudo easy_install -U fabric or,
   * sudo pip install fabric.

1. Run development setup script
   * python fabfile.py setup_development

1. Qualitio development environment is ready to use, lunch development
server
   * cd qualitio
   * python manage.py runserver

2. Setup Remote Production Environment (Debian/Ubuntu): 
-------------------------------------------------

In a case of using Debian sudo package is required. In some cases also
mercurial(hg) could be required.

1. Git clone this repository:
   * git clone git://github.com/qualitio/qualitio.git 
1. Download and install fabric:
   * sudo easy_install -U fabric
   if you don't have easy_install currently installed in your system
   you can find it in python-setuptools package
1. Go to cloned project directory, and run deployment script
   * cd qualtio
   * fab setup_production fab setup_production -H _{HOST}_
   where _{HOST}_ is address of your target machine, if you had plan
   deploy project locally simply type there _localhost_ (ssh server is
   required)

3. Updating Remote Production Environment (Debian/Ubuntu):
-------------------------------------------------
1. Go to cloned project directory, and run deployment script
   * cd qualtio
   * fab update_production -H _{HOST}_
   where _{HOST}_ is address of your target machine, if you had plan
   deploy project locally simply type there _localhost_ (ssh server is
   required)


4. Running Selenium Tests:
-------------------------------------------------
1. Before starting any testing you have to make sure that Java-jre is
installed (Selenium-RC test server is written used JAVA as running
platform).
1. Go to tests directory and start the Selenium-RC:
   * cd tests
   * java -jar selenium-server.jar
1. Run test suite 
   * python tests.py
   Check python tests.py for more available options
