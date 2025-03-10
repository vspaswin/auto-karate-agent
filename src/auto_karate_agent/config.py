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
        if not os.path.exists(cls.TEMPLATE_DIR):
            raise FileNotFoundError(f"Template directory not found at {cls.TEMPLATE_DIR}")
        if not os.path.exists(cls.KARATE_REPORT_DIR):
            raise FileNotFoundError(f"Karate report directory not found at {cls.KARATE_REPORT_DIR}")
        if not os.path.exists(cls.ALLURE_REPORT_DIR):
            raise FileNotFoundError(f"Allure report directory not found at {cls.ALLURE_REPORT_DIR}")