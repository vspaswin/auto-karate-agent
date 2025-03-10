import logging
from prance import ResolvingParser
from . import data_generator, template_manager, ai_integration, validators, security_tester
from .config import Config
from pathlib import Path

class OpenAPITestGenerator:
    def __init__(self):
        self.parser = ResolvingParser(Config.OPENAPI_PATH)
        self.endpoints = self._parse_endpoints()
        print(f"Found {len(self.endpoints)} endpoints")
        self.data_gen = data_generator.APIDataGenerator()
        self.template_mgr = template_manager.TemplateManager()
        self.ai = ai_integration.AITestGenerator()
        self.validator = validators.SchemaValidator()
        self.security_tester = security_tester.SecurityTestGenerator(self.parser)
        logging.basicConfig(level=logging.INFO)

    def _parse_endpoints(self):
        endpoints = []
        for path, methods in self.parser.specification['paths'].items():
            for method, details in methods.items():
                if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                    endpoints.append({
                        'path': path,
                        'method': method.upper(),
                        'operationId': details.get('operationId'),
                        'parameters': details.get('parameters', []),
                        'requestBody': details.get('requestBody', {}),
                        'responses': details.get('responses', {}),
                        'security': details.get('security', [])
                    })
        return endpoints

    def generate_all_tests(self):
        tests = []
        for path, methods in self.parser.specification.get('paths', {}).items():
            for method, endpoint in methods.items():
                # Enrich the endpoint with additional info if needed
                endpoint['path'] = path
                endpoint['method'] = method.upper()
                generated_tests = self._generate_endpoint_tests(endpoint)
            print(f"Tests generated for {method.upper()} {path}: {generated_tests}")
            tests.extend(generated_tests)
        return tests
    
    # def generate_all_tests(self):
    #     feature_files = []
    #     Path("features").mkdir(exist_ok=True)
        
    #     for endpoint in self.endpoints:
    #         tests = self._generate_endpoint_tests(endpoint)
    #         if tests:
    #         # Define filename only if tests exist
    #             filename = f"features/{endpoint['method']}_{endpoint['path'].replace('/', '_')}.feature"
    #             with open(filename, 'w') as f:
    #                 f.write(tests)
    #             feature_files.append(filename)  # Add to list only if file is created
        
    #     return feature_files


    # def _generate_endpoint_tests(self, endpoint):
    #     test_cases = []
        
    #     # Base scenarios
    #     test_cases.append(self._generate_positive_test(endpoint))
    #     test_cases.extend(self._generate_positive_test(endpoint))
    #     test_cases.extend(self.security_tester._generate_auth_tests(endpoint))
        
    #     # AI-generated tests
    #     if Config.AI_ENABLED:
    #         test_cases.extend(self.ai.generate_edge_cases(endpoint))
        
    #     # Request body tests
    #     test_cases.extend(self._generate_body_tests(endpoint))
        
    #     return self.template_mgr.render_tests(endpoint, test_cases)

    def _generate_endpoint_tests(self, endpoint):
        test_cases = []
        
        # Always generate basic endpoint test
        test_cases.append({
            'type': 'basic',
            'description': f"Basic {endpoint['method']} test",
            'expected_status': 200
        })
    
        # Add other tests (security, parameters, etc.)
        test_cases.extend(self.security_tester._generate_auth_tests(endpoint))
        test_cases.extend(self._generate_positive_test(endpoint))
        test_cases.extend(self._generate_body_tests(endpoint))
    
        # Format tests into Karate syntax
        if not test_cases:
            return ""  # Should never happen due to basic test
        
        feature_content = f"Feature: {endpoint['path']}\n\n"
        for test in test_cases:
            feature_content += f"Scenario: {test['description']}\n"
            feature_content += f"When method {endpoint['method']}\n"
            feature_content += f"Then status {test['expected_status']}\n\n"
        
        return feature_content
    
    def _generate_positive_test(self, endpoint):
            tests = []
            for param in endpoint.get('parameters', []):
                # Valid parameter
                tests.append({
                    'type': 'parameter',
                    'name': param['name'],
                    'value': self.data_gen.generate_valid_parameters([param]),
                    'expected_status': 200
                })
                
                # Edge cases
                for edge_value in self.data_gen.generate_edge_case(param):
                    tests.append({
                        'type': 'parameter_edge',
                        'name': param['name'],
                        'value': {param['name']: edge_value},
                        'expected_status': 400 if param.get('required') else 200
                    })
            return tests

    # def _generate_body_tests(self, endpoint):
    #     # Check if requestBody exists and has content
    #     if endpoint['method'] in ['POST', 'PUT', 'PATCH']:
    #         request_body = endpoint.get('requestBody')
    #         if not request_body:
    #             return []
                
    #         valid_body = self.data_gen.generate_edge_body(request_body)            
            
    #         return [
    #             {
    #                 'type': 'body_positive',
    #                 'body': valid_body,
    #                 'expected_status': 200
    #             }
    #         ]      
    
    def _generate_body_tests(self, endpoint):
        tests = []
        request_body = endpoint.get('requestBody', {})
        
        # Only generate body tests if requestBody exists with content
        if request_body and 'content' in request_body:
            content = request_body['content']
        if content:
            content_type = next(iter(content), 'application/json')
            schema = content[content_type].get('schema', {})
            if schema:
                valid_body = self.data_gen.generate_valid_body(request_body)
                tests.append({
                    'type': 'body_positive',
                    'body': valid_body,
                    'expected_status': 200
                })
        return tests