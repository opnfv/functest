#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import opnfv_testapi.cmd.server as swagger
from tornado.testing import AsyncHTTPTestCase
import unittest
import json


class GetSwaggerSpecs(AsyncHTTPTestCase):

        def get_app(self):
            return swagger.make_app()

        def test_swagger_documentation(self):
            response = self.fetch('/swagger/spec')
            self.assertEqual(response.code, 200)
            api_response = json.loads(response.body)
            response = self.fetch('/swagger/spec.json')
            self.assertEqual(response.code, 200)
            resource_response = json.loads(response.body)
            resource_response['models'] = api_response['models']
            resource_response['apis'] = api_response['apis']
            with open('specs.json', 'w') as outfile:
                json.dump(resource_response, outfile)

if __name__ == "__main__":
    unittest.main()
