from unittest.mock import patch
from src.auto_karate_agent.ai_integration import AITestGenerator
from config import Config

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