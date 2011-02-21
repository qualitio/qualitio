import unittest
import sys
import os
import time
import imp
import subprocess
from optparse import OptionParser

from config import settings #TODO: not very nice solution, an external module needed just to pass arguments

def __import__(name, globals=None, locals=None, fromlist=None):
    name = name.rstrip(".py") # just in case
    try:
        return sys.modules[name]
    except KeyError:
        pass
    fp, pathname, description = imp.find_module(name)

    try:
        return imp.load_module(name, fp, pathname, description)
    finally:
        if fp:
            fp.close()


def suite(test_suite_path):
    test_suite = __import__(test_suite_path)
    return unittest.TestLoader().loadTestsFromModule(test_suite)


if __name__ == "__main__":

    usage = "usage: %prog [options] test_suite_path"
    parser = OptionParser(usage)

    parser.add_option('-b', '--browser',
                      type='choice',
                      action='store',
                      dest='browser',
                      choices=['firefoxproxy', 'googlechrome', 'opera'],
                      default='firefoxproxy',
                      help='Browser environment to run on',)

    parser.add_option('-u', '--username',
                      type='string',
                      action='store',
                      dest='username',
                      default='',
                      help='Basic HTTP username',)

    parser.add_option('-p', '--password',
                      type='string',
                      action='store',
                      dest='password',
                      default='',
                      help='Basic HTTP password',)


    (options, args) = parser.parse_args()

    settings['hostname'] = 'http://127.0.0.1:8001'
    settings['username'] = options.username
    settings['password'] = options.password
    settings['browser'] = options.browser

    if len(args) != 1:
        parser.error("path to test siute is required")
    test_suite_path = args[0]

    with open("testing.log","wb") as out:
        selenium = subprocess.Popen(['java',
                                     '-jar',
                                     'selenium-server.jar'],
                                    stdout=out, stderr=subprocess.STDOUT)


        print "1. Starting Selenium server"

        print "2. Cleaning database"
        try:
            os.remove("selenium-test-data.sqlite")
        except OSError:
            pass

        syncdb = subprocess.Popen(['../qualitio/manage.py',
                                   'syncdb',
                                   '--noinput',
                                   '--settings=selenium_settings'],
                                    stdout=out, stderr=subprocess.STDOUT,
                                  shell=False
                                  )
        syncdb.wait()

        print "3. Starting application test server"
        runserver = subprocess.Popen(['../qualitio/manage.py',
                                      'runserver',
                                      '127.0.0.1:8001',
                                      '--settings=selenium_settings'],
                                     stdout=out, stderr=subprocess.STDOUT,
                                     shell=False)


        print "4. Starting tests"
        result = unittest.TextTestRunner(verbosity=2).run(suite(test_suite_path))

        # real kill for process child process
        selenium.kill()

        os.system("kill -9 `ps -o pid,ppid ax | awk '{ if ($2 == '%s' ) print $1}'`" %
                  runserver.pid)

        sys.exit(not result.wasSuccessful())
