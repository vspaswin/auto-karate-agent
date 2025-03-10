from test_generator.core import OpenAPITestGenerator
from prance import ResolvingParser

def test_endpoint_parsing():
    generator = OpenAPITestGenerator()
    generator.parser = ResolvingParser(spec_string="""
    openapi: 3.0.0
    paths:
      /users:
        get:
          responses: {}
    """)
    endpoints = generator._parse_endpoints()
    assert len(endpoints) == 1
    assert endpoints[0]['method'] == 'GET'