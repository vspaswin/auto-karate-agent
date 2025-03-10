# Regular tests
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# Performance tests
pytest tests/performance -v --benchmark-enable

# Security tests
pytest tests/security -v