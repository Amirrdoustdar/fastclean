from pathlib import Path
import re
from ...application.interfaces.validator import IValidator
from ...core.value_objects.project_config import ProjectConfig


class ProjectValidator(IValidator):
    """Project validator implementation"""
    
    # Reserved Python keywords
    RESERVED_KEYWORDS = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
        'while', 'with', 'yield'
    }
    
    def validate_project_name(self, name: str) -> bool:
        """Validate project name"""
        if not name:
            return False
        
        # Check if it's a valid Python identifier
        if not name.isidentifier():
            return False
        
        # Check if it's a reserved keyword
        if name in self.RESERVED_KEYWORDS:
            return False
        
        # Check if it starts with underscore (discouraged)
        if name.startswith('_'):
            return False
        
        return True
    
    def validate_path(self, path: Path) -> bool:
        """Validate path"""
        try:
            # Check if path is absolute or can be resolved
            resolved = path.resolve()
            
            # Check if parent directory exists or can be created
            if not resolved.parent.exists():
                # Try to check if we have permission to create it
                return self._check_write_permission(resolved.parent)
            
            return True
        except (OSError, RuntimeError):
            return False
    
    def validate_config(self, config: ProjectConfig) -> bool:
        """Validate project configuration"""
        # All enum values are already validated by Pydantic
        # Additional business rules can be added here
        return True
    
    @staticmethod
    def _check_write_permission(path: Path) -> bool:
        """Check if we have write permission to create path"""
        import os
        current = path
        while not current.exists():
            current = current.parent
        return os.access(current, os.W_OK)