
def main(request):
    from qualitio.organizations import OrganizationMember

    organization_member = None

    try:
        if request.user.is_authenticated():
            organization_member = request.user.organization_member.get(
                organization=request.organization
            )
    except AttributeError:
        pass

    return {"ROLE": {'ADMIN': OrganizationMember.ADMIN,
                     'USER': OrganizationMember.USER,
                     'USER_READONLY': OrganizationMember.USER_READONLY},
            "organization_member":     organization_member}
