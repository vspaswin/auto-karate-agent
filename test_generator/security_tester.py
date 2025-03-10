class SecurityTestGenerator:
    def __init__(self, parser):
        self.spec = parser.specification
        
    def generate_security_tests(self, endpoint):
        tests = []
        for scheme in endpoint.get('security', []):
            for auth_type in scheme:
                tests.extend(self._generate_auth_tests(auth_type))
        return tests
    
    def _generate_auth_tests(self, auth_type):
        return [
            {
                'type': 'security',
                'description': f'Missing {auth_type} credentials',
                'headers': {},
                'expected_status': 401
            },
            # ... other security scenarios ...
        ]