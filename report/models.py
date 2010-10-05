from django.db import models
from mptt.models import MPTTModel

class ReportDirectory(MPTTModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    name = models.CharField(max_length=256)

    def get_path(self):
        if self.get_ancestors():
            return "/%s/" % "/".join(map(lambda x: x.name, self.get_ancestors()))
        return "/"


    def __unicode__(self):
        return self.name


class Report(models.Model):
    directory = models.ForeignKey('ReportDirectory')

    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    public = models.BooleanField()
    context = models.TextField(blank=True)

    class Meta:
        unique_together = (("directory", "name"),)

    def get_path(self):
        if self.directory.get_ancestors():
            return "/%s/" % "/".join(map(lambda x: x.name, self.get_ancestors()))
        return "/"

    def __unicode__(self):
        return self.name

class Query(models.Model):
    report = models.ForeignKey('Report')

    name = models.CharField(max_length=512)
    definition = models.CharField(max_length=512)

    class Meta:
        unique_together = (("report", "name"),)
