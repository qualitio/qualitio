
def main(request):
    from qualitio.organizations import OrganizationMember

    organization_member = None

    try:
        if request.user.is_authenticated() and request.organization:
            organization_member = request.user.organization_member.get(
                organization=request.organization
            )
    except AttributeError:
        pass

    organization_url = ("%s://%s") % ("https" if request.is_secure() else "http",
                                      request.get_host())

    return {"ROLE": {'ADMIN': OrganizationMember.ADMIN,
                     'USER': OrganizationMember.USER,
                     'USER_READONLY': OrganizationMember.USER_READONLY},
            "organization_member": organization_member,
            "organization_url": organization_url}
