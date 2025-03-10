from jinja2 import Environment, FileSystemLoader
import os
from .config import Config

class TemplateManager:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(Config.TEMPLATE_DIR),
                              trim_blocks=True, lstrip_blocks=True)
        
    def render_tests(self, endpoint, test_cases):
        template = self._select_template(endpoint)
        return template.render({
            'endpoint': endpoint,
            'test_cases': test_cases,
            'utils': TemplateUtils()
        })

    def _select_template(self, endpoint):
        template_map = {
            'GET': 'read_template.feature.j2',
            'POST': 'crud_template.feature.j2',
            'PUT': 'crud_template.feature.j2',
            'DELETE': 'crud_template.feature.j2'
        }
        return self.env.get_template(template_map.get(endpoint['method'], 'default_template.feature.j2'))

class TemplateUtils:
    @staticmethod
    def karate_match(schema):
        if not schema:
            return '##null'
            
        schema_type = schema.get('type', 'object')
        fmt = schema.get('format', '')
        
        if schema_type == 'object':
            return {
                prop: TemplateUtils.karate_match(sub_schema)
                for prop, sub_schema in schema.get('properties', {}).items()
            }
            
        elif schema_type == 'array':
            return f'#[] {TemplateUtils.karate_match(schema.get("items"))}'
            
        type_map = {
            'string': '#string',
            'integer': '#number',
            'number': '#number',
            'boolean': '#boolean',
            'date': '#regex [0-9]{4}-[0-9]{2}-[0-9]{2}',
            'date-time': '#regex ^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}'
        }
        
        return type_map.get(fmt if fmt else schema_type, '##null')