import sys
from re import compile

from django import db
from django.conf import settings
from django.http import HttpResponseRedirect

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect('%s?next=%s' % (settings.LOGIN_URL, request.path_info) )


class QueriesCounterMiddleware:
    def process_request(self, request):
        if settings.DEBUG:
            db.reset_queries()

    def process_response(self, request, response):
        if settings.DEBUG:
            sys.stdout.write("Number of queries: %d " % len(db.connection.queries))
            sys.stdout.flush()
        return response
