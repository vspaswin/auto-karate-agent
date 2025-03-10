import openai
import json
import logging
from .config import Config

class AITestGenerator:
    def __init__(self):
        self.model = Config.OPENAI_MODEL
        
    def generate_edge_cases(self, endpoint):
        try:
            prompt = self._build_prompt(endpoint)
            response = self._query_ai(prompt)
            return self._parse_response(response)
        except Exception as e:
            logging.error(f"AI test generation failed: {str(e)}")
            return []

    def _query_ai(self, prompt):
        return openai.ChatCompletion.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=1500
        )

    def _parse_response(self, response):
        try:
            content = response.choices[0].message.content
            return json.loads(content)['scenarios']
        except json.JSONDecodeError:
            logging.error("Failed to parse AI response")
            return []
    
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