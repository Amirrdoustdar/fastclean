from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class FieldDefinition:
    """Field definition for entity"""
    name: str
    type: str
    required: bool = True
    default: str = None


@dataclass
class GenerateCRUDRequest:
    """Request for generating CRUD"""
    
    entity_name: str
    project_path: Path
    fields: list[FieldDefinition]
    generate_tests: bool = True


@dataclass
class GenerateCRUDResponse:
    """Response for CRUD generation"""
    
    entity_name: str
    files_created: list[Path]
    success: bool
    message: str