from test_generator.template_manager import TemplateUtils

def test_karate_match_string():
    schema = {"type": "string"}
    assert TemplateUtils.karate_match(schema) == "#string"

def test_karate_match_complex_object():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        }
    }
    result = TemplateUtils.karate_match(schema)
    assert result == {'name': '#string', 'age': '#number'}