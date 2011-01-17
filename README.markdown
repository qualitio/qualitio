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
   
