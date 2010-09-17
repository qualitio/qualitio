from django.contrib import admin
from treebeard.admin import TreeAdmin
from tcstorm_requirements.requirements.models import *

admin.site.register(Requirement, TreeAdmin)
