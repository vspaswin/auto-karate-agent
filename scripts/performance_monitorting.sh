# Generate performance report
pytest tests/performance --benchmark-enable --benchmark-json=perf.json

# Track over time
python -m pytest-benchmark compare perf.json --histogram=hist.svg