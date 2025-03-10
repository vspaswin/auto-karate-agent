import subprocess
from pathlib import Path

class TestRunner:
    @staticmethod
    def execute_tests(feature_files):
        for feature in feature_files:
            TestRunner._run_karate(feature)
            
    @staticmethod
    def _run_karate(feature_path):
        cmd = f"mvn test -Dtest=KarateRunner -Dkarate.options='{feature_path}'"
        subprocess.run(cmd, shell=True, check=True)