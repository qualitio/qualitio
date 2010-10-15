from django.db import models

from django.db import models
from treebeard.mp_tree import MP_Node


class Requirement(MP_Node):
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True)

    node_order_by = ['name']

    # Extra SQL for every get, no to good
    def get_path(self):
        if self.get_ancestors():
            return "/%s/" % "/".join(map(lambda x: x.name, self.get_ancestors()))
        return "/"

    def __unicode__(self):
        return 'Requirement: %s' % self.name


    def get_absolute_url(self):
        return "/require/" % self.id
