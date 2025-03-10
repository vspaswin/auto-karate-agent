import openai
import json
from ..config import Config

class AITestGenerator:
    def __init__(self):
        self.model = Config.OPENAI_MODEL
        
    def generate_edge_cases(self, endpoint):
        prompt = self._build_prompt(endpoint)
        response = self._query_ai(prompt)
        return self._parse_response(response)
    
    def _build_prompt(self, endpoint):
        return f"""Generate edge case test scenarios for this API endpoint:
        {json.dumps(endpoint, indent=2)}
        Consider these categories:
        - Invalid data types
        - Boundary values
        - Security vulnerabilities
        - Race conditions
        - Protocol violations
        """
    
    # ... (AI communication methods) ...