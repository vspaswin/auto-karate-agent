from src.auto_karate_agent.core import OpenAPITestGenerator
from test_runner import TestRunner
from config import Config

def main():
    Config.validate()
    
    generator = OpenAPITestGenerator()
    test_files = generator.generate_all_tests()
    
    TestRunner.execute_tests(test_files)
    
    print("Test generation and execution completed!")

if __name__ == "__main__":
    main()