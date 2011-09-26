# -*- coding: utf-8 -*-
from django import template


register = template.Library()


def has_permission(user, role):
    member = getattr(user, 'organization_member', None)
    if member and member.role <= role:
        return True
    return False
register.filter(has_permission)
