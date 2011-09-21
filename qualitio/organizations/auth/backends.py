from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from qualitio.organizations.models import OrganizationMember
from qualitio import THREAD


class OrganizationModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None):

        if THREAD.organization:
            try:
                organization_member = OrganizationMember.objects.get(user__username=username,
                                                                     organization=THREAD.organization,
                                                                     role__lt=OrganizationMember.INACTIVE)

                user = organization_member.user
                if user.check_password(password):
                    return user

            except OrganizationMember.DoesNotExist:
                return None

        else: # Except Organization url cases settings.ORGANIZATION_EXEMPT_URLS
            try:
                user = User.objects.get(username=username)
                if user.check_password(password) and user.is_staff:
                    return user

            except User.DoesNotExist:
                return None

