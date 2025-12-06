"""Setup configuration for fastapi-clean-cli"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path("README.md")
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

# Read requirements
requirements_file = Path("requirements.txt")
install_requires = []
if requirements_file.exists():
    install_requires = [
        line.strip() 
        for line in requirements_file.read_text().strip().split('\n')
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="fastapi-clean-cli",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="CLI tool for creating FastAPI projects with Clean Architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fastapi-clean-cli",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": ["*.j2", "*.yml", "*.yaml", "*.txt", "*.md"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "fastapi-clean=cli_main:main",
        ],
    },
)
