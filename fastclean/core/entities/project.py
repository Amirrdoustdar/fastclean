from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from .base import BaseEntity
from ..value_objects.project_config import ProjectConfig


@dataclass
class Project(BaseEntity):
    """Project entity representing a FastAPI project"""
    
    name: str
    path: Path
    config: ProjectConfig
    features: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__init__()
        self._validate()
    
    def _validate(self) -> None:
        """Validate project attributes"""
        if not self.name:
            raise ValueError("Project name cannot be empty")
        
        if not self.name.isidentifier():
            raise ValueError(
                f"Project name '{self.name}' is not a valid Python identifier"
            )
    
    def add_feature(self, feature_name: str) -> None:
        """Add a feature to the project"""
        if feature_name not in self.features:
            self.features.append(feature_name)
            self.update_timestamp()
    
    def has_feature(self, feature_name: str) -> bool:
        """Check if project has a specific feature"""
        return feature_name in self.features
    
    @property
    def full_path(self) -> Path:
        """Get full project path"""
        return self.path / self.name
