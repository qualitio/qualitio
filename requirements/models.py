from django.db import models

from django.db import models
from treebeard.mp_tree import MP_Node


class Requirement(MP_Node):
    name = models.CharField(max_length=30)

    node_order_by = ['name']

    def get_path(self):
        if self.get_ancestors():
            return "/%s/" % "/".join(map(lambda x: x.name, self.get_ancestors()))
        return "/"

    def __unicode__(self):
        return 'Requirement: %s' % self.name

