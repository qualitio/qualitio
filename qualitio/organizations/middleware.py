# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

from qualitio import THREAD


class OrganizationMiddleware(object):
    def process_request(self, request):
        THREAD.organization = None
        request.organization = None

        from qualitio.organizations import Organization, OrganizationMember
        
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

            if re.match('^/login/', request.get_full_path()):
                return redirect('organization_none')

        elif len(host_name_parts) == 3:
            try:
                organization = Organization.objects.get(slug=host_name_parts[0])

                THREAD.organization = organization
                request.organization = organization
            except Organization.DoesNotExist:
                raise Http404

        try:
            if request.user.is_authenticated() and request.organization:
                organization_member = request.user.organization_member.get(
                    organization=request.organization
                )
                request.organization_member = organization_member
        except OrganizationMember.DoesNotExist:
            pass

        return None

    def process_response(self, request, response):
        THREAD.organization = None
        request.organization = None
        return response


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

        try:
            project = Project.objects.get(organization=request.organization,
                                          slug=match.groupdict()['slug'])
        except Project.DoesNotExist:
            raise Http404

        THREAD.project = project
        request.project = project
        return None


    def process_response(self, request, response):
        THREAD.project = None
        request.project = None
        return response
