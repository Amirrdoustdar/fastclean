from pathlib import Path

# Version
VERSION = "1.0.0"
APP_NAME = "fastapi-clean-cli"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT.parent / "templates"

# File patterns
PYTHON_TEMPLATE_EXTENSION = ".py.j2"
YAML_TEMPLATE_EXTENSION = ".yml.j2"
TEXT_TEMPLATE_EXTENSION = ".txt.j2"

# Project structure
REQUIRED_DIRECTORIES = [
    "src/domain/entities",
    "src/domain/repositories",
    "src/application/usecases",
    "src/infrastructure/database",
    "src/interfaces/api/v1",
    "tests"
]

# Feature flags
AVAILABLE_FEATURES = {
    "auth": ["jwt", "oauth2", "api_key", "basic"],
    "cache": ["redis", "memcached", "in_memory"],
    "database": ["postgresql", "mysql", "sqlite", "mongodb"],
    "monitoring": ["prometheus", "elk"],
}