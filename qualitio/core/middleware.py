import sys
from re import compile

from django import db
from django.conf import settings
from django.utils import termcolors
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
        if settings.DEBUG and getattr(settings,"QUERIES_COUNTER", False):
            if not request.path.startswith(settings.MEDIA_URL):
                queries_count = len(db.connection.queries)
                color = "green"

                if queries_count > 20:
                    color = "red"
                elif queries_count > 10:
                    color = "yellow"

                log_lines = []
                log_lines.append("====== Response Debug ======")
                log_lines.append(termcolors.colorize("Number of queries: %d " % queries_count,
                                                     fg=color))

                if getattr(settings,"QUERIES_COUNTER_VERBOSE", False):
                    sql_queries = ["%s: %s" % (termcolors.colorize(str(i), fg=color), element.get("raw_sql")) for i, element in enumerate(db.connection.queries,1)]
                    log_lines.append("\n".join(sql_queries))

                sys.stderr.write("\n".join(log_lines))

        return response
