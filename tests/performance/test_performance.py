import pytest
from test_generator.core import OpenAPITestGenerator

@pytest.mark.benchmark
def test_generation_performance(benchmark):
    generator = OpenAPITestGenerator()
    
    # Benchmark test generation
    benchmark.pedantic(
        generator.generate_all_tests,
        iterations=5,
        rounds=3
    )
    
    # Assert reasonable execution time (adjust based on your needs)
    assert benchmark.stats.stats.max < 5.0  # Max 5 seconds