from django.utils.functional import wraps
from django.shortcuts import render_to_response


def permission_required(mode):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            from qualitio.projects.models import OrganizationMember

            role = getattr(OrganizationMember, mode, 999999)

            if not request.organization.members.filter(user=request.user, role__lte=role).exists():
                return render_to_response('core/permission_required.html', None)

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
