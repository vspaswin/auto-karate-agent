class SchemaValidator:
    def convert_to_karate_schema(self, openapi_schema):
        karate_rules = {}
        for prop, details in openapi_schema.get('properties', {}).items():
            karate_rules[prop] = self._type_to_karate(details)
        return karate_rules
    
    def _type_to_karate(self, schema):
        type_map = {
            'string': '#string',
            'integer': '#number',
            'boolean': '#boolean',
            'array': '#array'
        }
        return type_map.get(schema.get('type'), '##null')