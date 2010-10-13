from django.db import models

from treebeard.mp_tree import MP_Node

class TestRunDirectory(MP_Node):
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return 'TestRunDirectory: %s' % self.name

    def get_absolute_url(self):
        return "/execute/testrun/" % self.id


class TestRun(models.Model):
    name = models.CharField(max_length=512)


class TestCaseRun(models.Model):
    name = models.CharField(max_length=512)

    # origin Test Case
    # origin =
