from django.http import HttpResponse
from django.utils import simplejson as json

def json_response(func):
    def _jsonize(*args,**kwargs):
        return HttpResponse(json.dumps(func(*args,**kwargs), sort_keys=True, indent=2),
                        content_type='application/json; charset=UTF-8')
    return _jsonize


def success(message=""): 
    return { "success" : True,
             "message" : message }

def failed(message):
    return { "success" : False,
             "message" : message }
