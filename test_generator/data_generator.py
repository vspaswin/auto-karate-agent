from faker import Faker
import random
from datetime import datetime, timedelta

class APIDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.generated_data = {}

    def _generate_from_schema(self, schema):
        if 'example' in schema:
            return schema['example']
            
        schema_type = schema.get('type', 'object')
        fmt = schema.get('format', '')
        enum = schema.get('enum', [])
        min_val = schema.get('minimum', None)
        max_val = schema.get('maximum', None)
        
        if enum:
            return random.choice(enum)
            
        if schema_type == 'string':
            if fmt == 'email':
                return self.fake.email()
            elif fmt == 'date':
                return self.fake.date()
            elif fmt == 'date-time':
                return datetime.now().isoformat()
            elif fmt == 'uuid':
                return self.fake.uuid4()
            return self.fake.text(max_nb_chars=20)
            
        elif schema_type == 'integer':
            return random.randint(
                min_val if min_val is not None else 0,
                max_val if max_val is not None else 100
            )
            
        elif schema_type == 'boolean':
            return self.fake.boolean()
            
        elif schema_type == 'array':
            return [
                self._generate_from_schema(schema['items'])
                for _ in range(random.randint(1, 3))
            ]
            
        elif schema_type == 'object':
            return {
                prop: self._generate_from_schema(sub_schema)
                for prop, sub_schema in schema.get('properties', {}).items()
            }
            
        return None

    def generate_edge_case(self, param_schema):
        schema = param_schema.get('schema', {})
        edge_cases = []
        schema_type = schema.get('type', 'string')
        fmt = schema.get('format', '')
        
        # Type validation edges
        if schema_type == 'integer':
            edge_cases.extend([
                self.fake.word(),
                None,
                self.fake.pyfloat()
            ])
            if 'minimum' in schema:
                edge_cases.append(schema['minimum'] - 1)
            if 'maximum' in schema:
                edge_cases.append(schema['maximum'] + 1)
                
        elif schema_type == 'string':
            edge_cases.extend([
                None,
                self.fake.text(max_nb_chars=500),
                ""
            ])
            if fmt == 'email':
                edge_cases.append("invalid-email")
                
        elif schema_type == 'array':
            edge_cases.extend([
                None,
                [],
                [self.fake.word() for _ in range(100)]
            ])
            
        return edge_cases
    
    def generate_edge_body(self, schema):
            edge_body = self._generate_from_schema(schema)
            
            # Corrupt required fields
            if 'required' in schema:
                for field in schema['required']:
                    if field in edge_body:
                        del edge_body[field]
                        
            # Add extra fields
            edge_body['invalid_field'] = self.fake.word()
            
            return edge_body
    
    def _generate_from_schema(self, schema):
        if schema_type == 'array':
            # Add minimum/maximum items check
            min_items = schema.get('minItems', 1)
            max_items = schema.get('maxItems', 3)
            return [
                self._generate_from_schema(schema['items'])
                for _ in range(random.randint(min_items, max_items))
            ]
