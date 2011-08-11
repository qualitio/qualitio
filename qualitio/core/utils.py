from django.http import HttpResponse
from django.utils import simplejson as json
from dbtemplates.models import Template

def json_response(func):
    def _jsonize(*args,**kwargs):
        return HttpResponse(json.dumps(func(*args,**kwargs), sort_keys=True, indent=2),
                            content_type='application/json; charset=UTF-8')
    return _jsonize

def success(**kwargs):
    return { "success" : True,
             "message" : kwargs.get("message",""),
             "data" : kwargs.get("data","") }

def failed(**kwargs):
    return { "success" : False,
             "message" : kwargs.get("message",""),
             "data" : kwargs.get("data","") }

def load_dbtemplate(name):
    return lambda : (Template.objects.filter(name=name) or [''])[0]


class FieldList(list):
    def origin_append(self, item):
        super(FieldList, self).append(item)

    def append(self, item):
        new = FieldList(self)
        new.origin_append(item)
        return new

    def origin_extend(self, other_iterable):
        super(FieldList, self).extend(other_iterable)

    def extend(self, other_iterable):
        new = FieldList(self)
        new.origin_extend(other_iterable)
        return new

    def origin_insert(self, index, item):
        super(FieldList, self).insert(index, item)

    def insert(self, index, *items):
        new = FieldList(self)
        for i in xrange(len(items)):
            new.origin_insert(index + i, items[i])
        return new
