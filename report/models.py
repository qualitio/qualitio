from django.db import models
from mptt.models import MPTTModel

class ReportDirectory(MPTTModel):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    name = models.CharField(max_length=256)

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

    def __unicode__(self):
        return self.name
    
class Query(models.Model):
    report = models.ForeignKey('Report')
    
    name = models.CharField(max_length=256)
    definition = models.TextField(blank=True)
    
    class Meta:
        unique_together = (("report", "name"),)
