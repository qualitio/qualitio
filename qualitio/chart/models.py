# -*- coding: utf-8 -*-
from django.utils.importlib import import_module
from django.db import models

from qualitio.core.models import BaseModel


class ChartQuery(BaseModel):
    name = models.CharField(max_length=255)
    type_class_name = models.CharField(max_length=255)
    query = models.CharField(max_length=255)

    def get_type_class(self):
        splited = self.type_class_name.split('.')
        class_name = splited[-1]
        module = import_module('.'.join(splited[:-1]))
        return getattr(module, class_name)

    def __unicode__(self):
        return u"%s | %s" % (self.type_class_name, self.search_query)
