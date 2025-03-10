class SecurityTestGenerator:
    def __init__(self, parser):
        self.spec = parser.specification
        
    def _generate_auth_tests(self, auth_type):
    # Assuming auth_type is a dictionary with a 'method' key
        method = auth_type.get('method')
        security_scheme = self.spec['components']['securitySchemes'].get(method)

        if not security_scheme:
            raise ValueError(f"Security scheme for method '{method}' not found.")

        tests = []
        
        base_test = {
            'type': 'security',
            'auth_type': method,
            'expected_status': 401
        }
        
        if security_scheme['type'] == 'http':
            if security_scheme['scheme'] == 'bearer':
                tests.append({
                    **base_test,
                    'description': f'Missing {method} Bearer Token',
                    'headers': {'Authorization': ''}
                })
                tests.append({
                    **base_test,
                    'description': f'Invalid {method} Token',
                    'headers': {'Authorization': 'Bearer <placeholder>'},
                    'expected_status': 403
                })
                
        elif security_scheme['type'] == 'apiKey':
            tests.append({
                **base_test,
                'description': f'Missing {method} API Key',
                'headers': {}
            })
            tests.append({
                **base_test,
                'description': f'Invalid {method} API Key',
                'headers': {security_scheme['name']: 'invalid-key'},
                'expected_status': 403
            })
            
        return tests