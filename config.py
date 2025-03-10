import os

class Config:
    OPENAPI_PATH = 'openapi.yaml'
    TEMPLATE_DIR = 'templates'
    AI_ENABLED = False
    OPENAI_MODEL = "gpt-4"
    KARATE_REPORT_DIR = os.path.abspath('target/karate-reports')
    ALLURE_REPORT_DIR = os.path.abspath('target/allure-resports')
    
    @classmethod
    def validate(cls):
        if not os.path.exists(cls.OPENAPI_PATH):
            raise FileNotFoundError(f"OpenAPI spec not found at {cls.OPENAPI_PATH}")