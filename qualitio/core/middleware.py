import sys
import re

from django import db
from django.conf import settings
from django.utils import termcolors
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

EXEMPT_URLS = []
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    for pattern in settings.LOGIN_EXEMPT_URLS:
        if isinstance(pattern, list) or isinstance(pattern, tuple):
            expr = re.compile(pattern[0]), pattern[1]
        else:
            expr = re.compile(pattern), lambda request:True

        EXEMPT_URLS.append(expr)


class LoginRequiredMiddleware(object):
    def process_request(self, request):
        user = request.user
        path = request.path_info.lstrip('/')

        rules = map(lambda (pattern, condition): (pattern.match(path) is not None and condition(request)), EXEMPT_URLS)

        if any(rules):
            return None

        if user.is_authenticated():
            from qualitio.organizations.models import OrganizationMember

            if user.organization_member.get(organization=request.organization) == OrganizationMember.INACTIVE:
                return redirect('inactive')

            return None

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
                    sql_queries = ["%s: %s" % (termcolors.colorize(str(i), fg=color), element.get("sql")) for i, element in enumerate(db.connection.queries,1)]
                    log_lines.append("\n".join(sql_queries))

                sys.stderr.write("\n".join(log_lines))

        return response
