# -*- coding: utf-8 -*-
from django import template
from qualitio.organizations import OrganizationMember


register = template.Library()


def has_permission(user, role):
    """
    has_permission filter has ability to check if user has given permission.
    It can be used in two ways:

    1) if your template is processed with organization_roles context processor
       you use it following way:

    >>>
    >>> {% if not user|has_permission:ROLE.USER %} ...
    >>>

    2) if there's no organization_roles context processor (so ROLE dict is not avaiable)
       you can use a string:

    >>>
    >>> {% if not user|has_permission:"USER" %}
    >>>

    """
    try:
        role = int(role)
    except ValueError:
        role = getattr(OrganizationMember, role, OrganizationMember.USER_READONLY)

    related = getattr(user, 'organization_member', None)
    if related:
        member = (related.filter(user=user) or [None])[0]
        if member and member.role <= role:
            return True
    return False
register.filter(has_permission)
