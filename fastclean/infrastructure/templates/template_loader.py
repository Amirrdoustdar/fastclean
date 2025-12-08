from pathlib import Path
from typing import Dict, Optional
from ...core.entities.template import Template


class TemplateCache:
    """Cache for loaded templates"""
    
    def __init__(self):
        self._cache: dict[str, Template] = {}
    
    def get(self, key: str) -> Optional[Template]:
        """Get template from cache"""
        return self._cache.get(key)
    
    def set(self, key: str, template: Template) -> None:
        """Set template in cache"""
        self._cache[key] = template
    
    def clear(self) -> None:
        """Clear cache"""
        self._cache.clear()
    
    def has(self, key: str) -> bool:
        """Check if template is in cache"""
        return key in self._cache
    
    @staticmethod
    def make_key(template_name: str, category: str) -> str:
        """Make cache key"""
        return f"{category}:{template_name}"
