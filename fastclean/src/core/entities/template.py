from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
from .base import BaseEntity


@dataclass
class Template(BaseEntity):
    """Template entity for code generation"""
    
    name: str
    content: str
    variables: Dict[str, str]
    category: str
    output_path: Optional[Path] = None
    
    def __post_init__(self):
        super().__init__()
    
    def render_path(self, context: Dict[str, str]) -> Path:
        """Render output path with context variables"""
        if not self.output_path:
            return Path(self.name)
        
        path_str = str(self.output_path)
        for key, value in context.items():
            path_str = path_str.replace(f"{{{{{key}}}}}", value)
        
        return Path(path_str)
    
    def get_required_variables(self) -> List[str]:
        """Get list of required variables for this template"""
        return list(self.variables.keys())
