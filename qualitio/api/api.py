from django.contrib.auth.models import User
from tastypie.resources import ModelResource


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
