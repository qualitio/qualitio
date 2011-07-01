REST API
========

Qualitio api example scripts.
All used examples use reskit library http://pypi.python.org/pypi/restkit/


Example 1. Gets all objects from resource(GET)

.. code-block:: python


   import json
   from pprint import pprint
   from restkit import request

   req = request("http://admin:admin@127.0.0.1:8000/api/require/requirement/")
   response = req.body_string()

   pprint( json.loads(response) )



Example2. - Gets one object(GET)


.. code-block:: python

   import json
   from pprint import pprint
   from restkit import request

   req = request("http://admin:admin@127.0.0.1:8000/api/require/requirement/1/")
   response = req.body_string()

   pprint( json.loads(response) )



Example3. Modifies object(PUT)

.. code-block:: python

   import json
   from restkit import Resource

   resource = Resource('http://admin:admin@127.0.0.1:8000/api', )
   response = resource.put('/require/requirement/1/',
                          headers={'Content-type': 'application/json'},
                          payload=json.dumps({"name": "New name"}))
   print response.body_string()



Example4. Creates object(POST)

.. code-block:: python

   import json
   from restkit import Resource

   resource = Resource('http://admin:admin@127.0.0.1:8000/api', )
   response = resource.post('/require/requirement/',
                            headers={'Content-type': 'application/json'},
                            payload=json.dumps({"name": "ALA2",
                                                "parent": "/api/require/requirement/1/"}))

   print response.body_string()
