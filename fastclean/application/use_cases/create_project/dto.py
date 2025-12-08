from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from fastclean.core.value_objects.project_config import ProjectConfig


@dataclass
class CreateProjectRequest:
    """Request DTO for creating a project"""
    
    name: str
    path: Path
    config: ProjectConfig


@dataclass
class CreateProjectResponse:
    """Response DTO for creating a project"""
    
    project_id: str
    project_name: str
    project_path: Path
    files_created: int
    success: bool
    message: str
