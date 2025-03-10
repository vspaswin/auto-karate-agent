import pytest
from test_generator.core import OpenAPITestGenerator

def test_full_generation_cycle(tmp_path):
    # Test the complete generate → save → execute flow
    generator = OpenAPITestGenerator()
    test_files = generator.generate_all_tests()
    
    assert len(test_files) > 0
    assert all(f.endswith('.feature') for f in test_files)
    
    # Verify files contain valid Karate syntax
    for f in test_files:
        with open(f) as feature_file:
            content = feature_file.read()
            assert "Feature:" in content
            assert "Scenario:" in content