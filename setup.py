from setuptools import setup, find_packages

setup(
    name="auto-karate-agent",
    version="0.1.0",
    description="Autonomous AI Agent for generating Karate DSL tests",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "prance>=0.21.8",
        "openapi-spec-validator",
        "faker>=18.11.2",
        "jinja2>=3.1.2",
        "openai>=0.27.8",
        "pyyaml>=6.0",
        "pytest>=7.0.0",
        "pytest-mock>=3.0.0",
        "pytest-benchmark>=4.0.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,  # ✅ Only declare this once
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)