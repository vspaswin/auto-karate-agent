from jinja2 import Environment, FileSystemLoader
import os

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
        # ... (schema to Karate match helpers) ...