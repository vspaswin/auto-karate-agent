import json
import yaml
from faker import Faker
from prance import ResolvingParser
import openai
import os
import logging
import itertools

class OpenAPITestGenerator:
    def __init__(self, openapi_path):
        self.fake = Faker()
        self.parser = ResolvingParser(openapi_path)
        self.endpoints = self._parse_endpoints()
        self.ai_enabled = True
        logging.basicConfig(level=logging.INFO)

    def _parse_endpoints(self):
        endpoints = []
        for path, methods in self.parser.specification['paths'].items():
            for method, details in methods.items():
                if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                    endpoints.append({
                        'path': path,
                        'method': method.upper(),
                        'parameters': details.get('parameters', []),
                        'requestBody': details.get('requestBody', {}),
                        'responses': details.get('responses', {})
                    })
        return endpoints

    def generate_synthetic_data(self, schema):
        if 'schema' not in schema:
            return None
            
        return self._generate_from_schema(schema['schema'])

    def _generate_from_schema(self, schema):
        if 'example' in schema:
            return schema['example']

        schema_type = schema.get('type', 'object')
        formats = schema.get('format', '')
        enum = schema.get('enum', [])
        
        if enum:
            return self.fake.random_element(enum)
        
        if schema_type == 'string':
            if formats == 'email':
                return self.fake.email()
            elif formats == 'date':
                return self.fake.date()
            return self.fake.word()
        elif schema_type == 'integer':
            min_val = schema.get('minimum', 0)
            max_val = schema.get('maximum', 1000)
            return self.fake.random_int(min=min_val, max=max_val)
        elif schema_type == 'boolean':
            return self.fake.boolean()
        elif schema_type == 'array':
            return [self._generate_from_schema(schema['items'])]
        elif schema_type == 'object':
            return {k: self._generate_from_schema(v) for k, v in schema.get('properties', {}).items()}
        return None

    def _generate_edge_cases(self, param):
        edge_cases = []
        param_type = param.get('schema', {}).get('type', 'string')
        
        # Generate boundary values and invalid types
        if param_type == 'integer':
            edge_cases.extend([
                param.get('schema', {}).get('minimum', 0) - 1,
                param.get('schema', {}).get('maximum', 100) + 1,
                self.fake.word()
            ])
        elif param_type == 'string':
            edge_cases.extend([
                self.fake.text(max_nb_chars=500),
                '',
                self.fake.random_number()
            ])
        elif param_type == 'boolean':
            edge_cases.extend(['true', 'false', 1, 0])
        
        return edge_cases

    def _generate_ai_edge_cases(self, endpoint):
        if not self.ai_enabled:
            return []
            
        prompt = f"""Generate 5 edge case test scenarios for this API endpoint:
        {json.dumps(endpoint, indent=2)}
        Return scenarios in JSON format with description and parameters."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logging.error(f"AI Error: {str(e)}")
            return []

    def generate_tests(self):
        feature_files = []
        
        for endpoint in self.endpoints:
            feature_content = f"Feature: Test {endpoint['method']} {endpoint['path']}\n"
            scenarios = []
            
            # Positive test scenario
            positive_params = {}
            for param in endpoint['parameters']:
                if param['in'] == 'path':
                    positive_params[param['name']] = self.generate_synthetic_data(param)
            
            scenarios.append({
                'name': 'Valid Request',
                'params': positive_params,
                'status': 200
            })

            # Parameter edge cases
            for param in endpoint['parameters']:
                for edge_value in self._generate_edge_cases(param):
                    edge_params = positive_params.copy()
                    edge_params[param['name']] = edge_value
                    scenarios.append({
                        'name': f"Edge Case - {param['name']} ({edge_value})",
                        'params': edge_params,
                        'status': 400 if param.get('required', False) else 200
                    })

            # AI-generated edge cases
            for ai_scenario in self._generate_ai_edge_cases(endpoint):
                scenarios.append({
                    'name': f"AI Generated - {ai_scenario['description']}",
                    'params': ai_scenario['parameters'],
                    'status': ai_scenario.get('expected_status', 400)
                })

            # Request body tests
            if endpoint['requestBody']:
                content_type = next(iter(endpoint['requestBody'].get('content', {})), 'application/json')
                valid_body = self.generate_synthetic_data(
                    endpoint['requestBody']['content'][content_type]
                )
                scenarios.append({
                    'name': 'Valid Request Body',
                    'body': valid_body,
                    'status': 200
                })

            # Build Karate scenarios
            for scenario in scenarios:
                feature_content += f"\n  Scenario: {scenario['name']}\n"
                feature_content += f"    Given url '{endpoint['path']}'\n"
                
                if 'params' in scenario:
                    for name, value in scenario['params'].items():
                        feature_content += f"    And path {name} = {json.dumps(value)}\n"
                
                if 'body' in scenario:
                    feature_content += f"    And request {json.dumps(scenario['body'], indent=4)}\n"
                
                feature_content += f"    When method {endpoint['method'].lower()}\n"
                feature_content += f"    Then status {scenario['status']}\n"
                
                if scenario['status'] == 200:
                    feature_content += "    And match response != null\n"

            filename = f"{endpoint['method']}_{endpoint['path'].replace('/', '_')}.feature"
            with open(filename, 'w') as f:
                f.write(feature_content)
            feature_files.append(filename)
            logging.info(f"Generated {filename}")

        return feature_files

    def execute_tests(self):
        for feature_file in self.generate_tests():
            os.system(f"mvn test -Dtest=KarateRunner -Dkarate.options='--tags @{feature_file}'")

if __name__ == "__main__":
    # Initialize with your OpenAPI spec
    generator = OpenAPITestGenerator('openapi.yaml')
    
    # Configure OpenAI (optional)
    generator.ai_enabled = False
    # openai.api_key = 'your-api-key'
    
    # Generate and execute tests
    generator.execute_tests()