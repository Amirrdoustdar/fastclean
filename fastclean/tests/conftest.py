import pytest
import asyncio
from typing import Generator
from pathlib import Path


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_project_path(tmp_path: Path) -> Path:
    """Temporary path for project generation tests."""
    return tmp_path / "test_project"


@pytest.fixture
def sample_project_config() -> dict:
    """Sample project configuration for testing."""
    return {
        "name": "test_project",
        "db": "postgresql",
        "auth": "jwt",
        "cache": "redis",
        "docker": True,
    }


@pytest.fixture
def sample_entity_config() -> dict:
    """Sample entity configuration for testing."""
    return {
        "name": "Product",
        "fields": "name:str,price:float,quantity:int",
    }
