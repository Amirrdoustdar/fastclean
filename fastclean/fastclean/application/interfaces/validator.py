from abc import ABC, abstractmethod
from pathlib import Path

from ...core.value_objects.project_config import ProjectConfig


class IValidator(ABC):
    """Interface for validation operations"""

    @abstractmethod
    def validate_project_name(self, name: str) -> bool:
        """Validate project name"""

    @abstractmethod
    def validate_path(self, path: Path) -> bool:
        """Validate path"""

    @abstractmethod
    def validate_config(self, config: ProjectConfig) -> bool:
        """Validate project configuration"""
