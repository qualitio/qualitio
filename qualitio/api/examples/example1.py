import json
from pprint import pprint
from restkit import request

req = request("http://admin:admin@127.0.0.1:8000/api/require/requirement/")
response = req.body_string()

pprint( json.loads(response) )
