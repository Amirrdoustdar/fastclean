from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
from .base import BaseEntity


@dataclass
class Template(BaseEntity):
    """Template entity for code generation"""
    
    name: str
    content: str
    variables: dict
    category: str
    output_path: Optional[Path] = None
    
    def __post_init__(self):
        super().__init__()
    
    def render_path(self, context: Dict[str, Any]) -> Path:
        """Render output path with context variables"""
        if not self.output_path:
            return Path(self.name)
        
        path_str = str(self.output_path)
        for key, value in context.items():
            # Convert value to string
            path_str = path_str.replace(f"{{{{{key}}}}}", str(value))
        
        return Path(path_str)
    
    def get_required_variables(self) -> list:
        """Get list of required variables for this template"""
        return list(self.variables.keys())