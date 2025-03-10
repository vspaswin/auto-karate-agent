import pytest
from auto_karate_agent.core import OpenAPITestGenerator

@pytest.mark.benchmark
def test_generation_performance(benchmark):
    def setup():
        return OpenAPITestGenerator(),  
    
    # Benchmark test generation
    benchmark.pedantic(OpenAPITestGenerator.generate_all_tests, setup=setup)
    
    # Assert reasonable execution time (adjust based on your needs)
    assert benchmark.stats.stats.max < 5.0  # Max 5 seconds