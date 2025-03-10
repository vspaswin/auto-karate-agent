from unittest.mock import patch
from test_generator.ai_integration import AITestGenerator

@patch('openai.ChatCompletion.create')
def test_ai_edge_case_generation(mock_openai):
    mock_openai.return_value = {
        "choices": [{
            "message": {"content": '{"scenarios": [{"description": "Test"}]}'}
        }]
    }
    
    ai = AITestGenerator()
    result = ai.generate_edge_cases({})
    assert len(result) == 1
    assert result[0]['description'] == "Test"