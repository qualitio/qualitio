from django.db import models
from django.contrib.contenttypes.models import ContentType

from qualitio.core import BaseModel


class FilterQuery(BaseModel):
    name = models.CharField(max_length=255)
    query = models.TextField(null=True, blank=True)
    contenttype = models.ForeignKey(ContentType, null=True)

    class Meta:
        unique_together = ("name", "contenttype")

    def __unicode__(self):
        return u'%s | %s' % (
            self.contenttype.model_class() if self.contenttype else '',
            self.name)
