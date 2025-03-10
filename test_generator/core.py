import logging
from prance import ResolvingParser
from . import data_generator, template_manager, ai_integration, validators, security_tester

class OpenAPITestGenerator:
    def __init__(self):
        self.parser = ResolvingParser(Config.OPENAPI_PATH)
        self.endpoints = self._parse_endpoints()
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
        for endpoint in self.endpoints:
            tests.extend(self._generate_endpoint_tests(endpoint))
        return tests

    def _generate_endpoint_tests(self, endpoint):
        test_cases = []
        
        # Base scenarios
        test_cases.append(self._generate_positive_test(endpoint))
        test_cases.extend(self._generate_parameter_tests(endpoint))
        test_cases.extend(self.security_tester.generate_security_tests(endpoint))
        
        # AI-generated tests
        if Config.AI_ENABLED:
            test_cases.extend(self.ai.generate_edge_cases(endpoint))
        
        # Request body tests
        test_cases.extend(self._generate_body_tests(endpoint))
        
        return self.template_mgr.render_tests(endpoint, test_cases)

    def _generate_positive_test(self, endpoint):
        return {
            'type': 'positive',
            'parameters': self.data_gen.generate_valid_parameters(endpoint['parameters']),
            'body': self.data_gen.generate_valid_body(endpoint.get('requestBody')),
            'expected_status': 200
        }
    
    # ... (other test generation methods) ...