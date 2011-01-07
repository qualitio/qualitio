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
