import ast
from pathlib import Path

def test_no_secrets_in_code():
    # Scan all Python files for potential secrets
    secrets = ['password', 'secret', 'api_key', 'token']
    files = Path('test_generator').rglob('*.py')
    
    for file in files:
        with open(file) as f:
            content = f.read().lower()
            for secret in secrets:
                assert secret not in content, f"Potential secret leak in {file}"