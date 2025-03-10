import re
from pathlib import Path

class CodeScanner:
    SECRET_PATTERN = re.compile(
        r'(?:password|secret|api[ _-]?key|token)["\']?\s*[:=]\s*["\'].+["\']',
        re.IGNORECASE
    )

    @classmethod
    def find_secrets(cls, directory='test_generator'):
        issues = []
        for path in Path(directory).rglob('*.py'):
            with open(path) as f:
                for i, line in enumerate(f, 1):
                    if cls.SECRET_PATTERN.search(line):
                        issues.append(f"Potential secret in {path}:{i}")
        return issues