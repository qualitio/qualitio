import json
from restkit import Resource

resource = Resource('http://admin:admin@127.0.0.1:8000/api', )
response = resource.post('/require/requirement/',
                         headers={'Content-type': 'application/json'},
                         payload=json.dumps({"name": "ALA2",
                                             "parent": "/api/require/requirement/1/"}))

print response.body_string()
