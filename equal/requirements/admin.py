from django.contrib import admin
from treebeard.admin import TreeAdmin
from equal.requirements.models import *

admin.site.register(Requirement, TreeAdmin)
