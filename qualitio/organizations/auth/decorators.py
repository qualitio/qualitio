from django.utils.functional import wraps
from django.shortcuts import render_to_response


def permission_required(mode):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            from qualitio.organizations.models import OrganizationMember

            role = getattr(OrganizationMember, mode, 999999)
            if not request.organization.members.filter(pk=request.user.pk,
                                                       organization_member__role__lt=role).exists():
                return render_to_response('core/permission_required.html', None)

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
