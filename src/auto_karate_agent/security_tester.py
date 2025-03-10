class SecurityTestGenerator:
    def __init__(self, parser):
        self.spec = parser.specification
        
    def _generate_auth_tests(self, endpoint):
        # Extract the security requirements from the endpoint
        print("Endpoint: ", endpoint)
        security_reqs = endpoint.get('security', [])
        if not security_reqs:
            print("No security requirements found for endpoint:", endpoint)
            return []  # or handle the absence of security definitions appropriately

        # Assuming you want to work with the first security requirement:
        scheme_name = list(security_reqs[0].keys())[0]
        security_scheme = self.spec['components']['securitySchemes'].get(scheme_name)
        
        if not security_scheme:
            raise ValueError(f"Security scheme for '{scheme_name}' not found.")
        
        method = endpoint['method']
        tests = []
        
        print("Security scheme type:", security_scheme['type'])
        
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