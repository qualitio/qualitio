from django.db import models
from django.contrib.auth.models import User

# class ProjectAware(models.Model):
#     """
#     A mixin abstract base model to use on models you want to make project-aware.
#     """

#     project_content_type = models.ForeignKey(ContentType, null=True, blank=True)
#     project_object_id = models.PositiveIntegerField(null=True, blank=True)
#     project = generic.GenericForeignKey("group_content_type", "group_object_id")

#     class Meta:
#         abstract = True


# class OwnerShipAware(models.Model):
#     owner =
#     team =
#     modifier =

#     created_time =
#     modified_time =

# class Team(ProjectAware):
#     pass

# class User

class Team(models.Model):
    name = models.CharField(max_length=250)
    users = models.ManyToManyField(User, related_name="users")
    leader = models.ForeignKey(User, related_name="leader")
                               # limit=limit_choices_to = {'pub_date__lte': datetime.now})

class UserProfile(models.Model):
    pass


