Qualitio Project
================

1. Setup Development Environment (Debian/Ubuntu): 
-------------------------------------------------

1. Install python-setuptools and python-dev packages
   * sudo apt-get install python-setuptools python-dev

1. Download and install fabric:
   * sudo easy_install -U fabric

1. Git clone this repository:
   * git clone git://github.com/qualitio/qualitio.git 

1. Go to repository directory and run development setup script
   * cd qualtio
   * fab setup_development

1. Go to project directory and sync your base
   * cd qualtio
   * python manage.py syncdb


2. Setup Remote Production Environment (Debian/Ubuntu): 
-------------------------------------------------
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
1. Go to cloned project directory, and run deployment script
   * cd qualtio
   * fab setup_production fab update_production -H _{HOST}_
   where _{HOST}_ is address of your target machine, if you had plan
   deploy project locally simply type there _localhost_ (ssh server is
   required)


4. Setup Running Selenium Tests:
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
