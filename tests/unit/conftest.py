import pytest
from faker import Faker
from test_generator.data_generator import APIDataGenerator

@pytest.fixture
def sample_schema():
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 18}
        },
        "required": ["name"]
    }

@pytest.fixture
def data_generator():
    return APIDataGenerator()