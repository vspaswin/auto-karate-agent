class SecurityTestGenerator:
    def __init__(self, parser):
        self.spec = parser.specification
        
    def _generate_auth_tests(self, auth_type):
        security_scheme = self.spec['components']['securitySchemes'][auth_type]
        tests = []
        
        base_test = {
            'type': 'security',
            'auth_type': auth_type,
            'expected_status': 401
        }
        
        if security_scheme['type'] == 'http':
            if security_scheme['scheme'] == 'bearer':
                tests.append({
                    **base_test,
                    'description': f'Missing {auth_type} Bearer Token',
                    'headers': {'Authorization': ''}
                })
                tests.append({
                    **base_test,
                    'description': f'Invalid {auth_type} Token',
                    'headers': {'Authorization': 'Bearer invalid_token'},
                    'expected_status': 403
                })
                
        elif security_scheme['type'] == 'apiKey':
            tests.append({
                **base_test,
                'description': f'Missing {auth_type} API Key',
                'headers': {}
            })
            tests.append({
                **base_test,
                'description': f'Invalid {auth_type} API Key',
                'headers': {security_scheme['name']: 'invalid-key'},
                'expected_status': 403
            })
            
        elif security_scheme['type'] == 'oauth2':
             tests.append({
            **base_test,
            'description': f'Invalid {auth_type} OAuth Token',
            'headers': {'Authorization': 'Bearer invalid_oauth_token'},
            'expected_status': 403
    })
            
        return tests