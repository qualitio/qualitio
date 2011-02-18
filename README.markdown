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

3. Setup Running Selenium Tests:
-------------------------------------------------
1. Before starting any tests you must start the Selenium server.
   Go to tests directory where Selenium-RC’s server is located 
   (qualitio/tests/selenium-server-1.0.3) and run the following from a command-line console.
   * java -jar selenium-server.jar
1. Go to tests directory and run tests with options:
   * python tests.py <options>
   Options:
  -h, --help            show this help message and exit
  -b BROWSER, --browser=BROWSER
                        Browser environment to run on
  -u USERNAME, --username=USERNAME
                        Basic HTTP username
  -p PASSWORD, --password=PASSWORD
                        Basic HTTP password

