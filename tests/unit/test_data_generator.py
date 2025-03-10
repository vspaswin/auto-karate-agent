def test_generate_valid_parameters(data_generator):
    params = [{
        "name": "userId",
        "in": "path",
        "required": True,
        "schema": {"type": "integer"}
    }]
    
    result = data_generator.generate_valid_parameters(params)
    assert isinstance(result['userId'], int)
    assert result['userId'] >= 0

def test_edge_case_generation(data_generator):
    schema = {"type": "string", "format": "email"}
    edge_cases = data_generator.generate_edge_case({"schema": schema})
    assert "invalid-email" in edge_cases
    assert None in edge_cases