import json
from restkit import Resource

resource = Resource('http://admin:admin@127.0.0.1:8000/api', )
response = resource.put('/require/requirement/1/',
                        headers={'Content-type': 'application/json'},
                        payload=json.dumps({"name": "New name"}))
print response.body_string()
