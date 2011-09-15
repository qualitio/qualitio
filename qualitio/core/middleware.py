import sys
import re

from django import db
from django.conf import settings
from django.utils import termcolors
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ImproperlyConfigured


EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


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
                    sql_queries = ["%s: %s" % (termcolors.colorize(str(i), fg=color), element.get("sql")) for i, element in enumerate(db.connection.queries,1)]
                    log_lines.append("\n".join(sql_queries))

                sys.stderr.write("\n".join(log_lines))

        return response


from threading import local


PROJECT_MATCH = r'^project/(?P<project>[\w-]+).*'
PROJECT_EXEMPT_URLS = [re.compile(PROJECT_MATCH)]
if hasattr(settings, 'PROJECT_EXEMPT_URLS'):
    PROJECT_EXEMPT_URLS += [re.compile(expr) for expr in settings.PROJECT_EXEMPT_URLS]

THREAD = local()


class OrganizationMiddleware(object):
    def process_request(self, request):
        THREAD.organization = None
        request.organization = None

        from qualitio.organizations import Organization
        match = re.match('^(?P<host>[\w\.\-]+)(:(?P<port>\d+))?', request.get_host())
        if not match:
            raise ImproperlyConfigured("OrganizationMiddleware is running")

        host_name = match.groupdict()['host']

        host_name_parts = host_name.split(".")
        if len(host_name_parts) < 2:
            raise ImproperlyConfigured("OrganizationMiddleware is running")

        elif len(host_name_parts) == 2:
            THREAD.organization = None
            request.organization = None

        elif len(host_name_parts) == 3:
            try:
                organization = Organization.objects.get(slug=host_name_parts[0])

                THREAD.organization = organization
                request.organization = organization
            except Organization.DoesNotExist:
                raise Http404

        return None

    def process_response(self, request, response):
        THREAD.organization = None
        request.organization = None
        return response


class ProjectMiddleware(object):
    def process_request(self, request):
        THREAD.project = None
        request.project = None

        from qualitio.organizations import Project
        path = request.path_info.lstrip('/')

        if path.startswith("project/new/"):
            return None

        match = re.match(r'^project/(?P<slug>[\w-]+)', path)
        if not match:
            return None

        project = Project.objects.get(slug=match.groupdict()['slug'])

        THREAD.project = project
        request.project = project
        return None


    def process_response(self, request, response):
        THREAD.project = None
        request.project = None
        return response

