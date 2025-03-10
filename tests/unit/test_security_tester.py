from prance import ResolvingParser
from auto_karate_agent.security_tester import SecurityTestGenerator

def test_api_key_security():
    parser = ResolvingParser(spec_string="""
    openapi: 3.0.0
    components:
      securitySchemes:
        ApiKeyAuth:
          type: apiKey
          name: X-API-KEY
          in: header
    """)
    tester = SecurityTestGenerator(parser)
    tests = tester._generate_auth_tests('ApiKeyAuth')
    assert len(tests) == 2
    assert tests[0]['description'] == "Missing ApiKeyAuth API Key"