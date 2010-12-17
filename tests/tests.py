import unittest
import sys

from optparse import OptionParser
from require.browse import tests
from config import settings #TODO: not very nice solution, an external module needed just to pass arguments

def suite():
    return unittest.TestLoader().loadTestsFromModule(tests)

if __name__ == "__main__":

    usage = "usage: %prog [options] url"
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
    if len(args) != 1:
         parser.error("url adres of testing site is required")
    
    settings['hostname'] = args[0]
    settings['username'] = options.username
    settings['password'] = options.password
    settings['browser'] = options.browser

    result = unittest.TextTestRunner(verbosity=2).run(suite())
    sys.exit(not result.wasSuccessful())
