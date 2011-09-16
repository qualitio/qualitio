def organization_roles(request):
    from qualitio.organizations import OrganizationMember
    return dict(ROLE={
            'ADMIN': OrganizationMember.ADMIN,
            'USER': OrganizationMember.USER,
            'USER_READONLY': OrganizationMember.USER_READONLY,
            })
