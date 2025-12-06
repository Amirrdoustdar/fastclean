from pathlib import Path
import os


class PathResolver:
    """Resolve and normalize paths"""
    
    @staticmethod
    def resolve(path: str | Path) -> Path:
        """Resolve path to absolute path"""
        p = Path(path)
        return p.expanduser().resolve()
    
    @staticmethod
    def get_project_root() -> Path:
        """Get project root directory"""
        return Path(__file__).parent.parent.parent
    
    @staticmethod
    def get_templates_dir() -> Path:
        """Get templates directory"""
        return PathResolver.get_project_root().parent / "templates"
    
    @staticmethod
    def normalize_project_name(name: str) -> str:
        """Normalize project name to valid identifier"""
        # Remove special characters, keep only alphanumeric and underscore
        import re
        normalized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure it doesn't start with a number
        if normalized[0].isdigit():
            normalized = f"_{normalized}"
        return normalized