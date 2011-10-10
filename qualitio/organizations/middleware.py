# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

from qualitio import THREAD


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


PROJECT_MATCH = r'^project/(?P<project>[\w-]+).*'
PROJECT_EXEMPT_URLS = [re.compile(PROJECT_MATCH)]
if hasattr(settings, 'PROJECT_EXEMPT_URLS'):
    PROJECT_EXEMPT_URLS += [re.compile(expr) for expr in settings.PROJECT_EXEMPT_URLS]


class ProjectMiddleware(object):
    """
    IMPORTANT! ProjectMiddleware need to be placed BEFORE OrganizationMiddleware
    since we decided that Project.name don't need to be unique.
    """

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

        project = Project.objects.get(organization=request.organization,
                                      slug=match.groupdict()['slug'])

        THREAD.project = project
        request.project = project
        return None


    def process_response(self, request, response):
        THREAD.project = None
        request.project = None
        return response
