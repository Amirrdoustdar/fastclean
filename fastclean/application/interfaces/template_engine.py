from abc import ABC, abstractmethod
from typing import Dict, Any
from ...core.entities.template import Template


class ITemplateEngine(ABC):
    """Interface for template rendering"""
    
    @abstractmethod
    def render(self, template: Template, context: dict[str, Any]) -> str:
        """Render template with context"""
        pass
    
    @abstractmethod
    def load_template(self, template_name: str, category: str) -> Template:
        """Load template by name and category"""
        pass
    
    @abstractmethod
    def list_templates(self, category: str) -> list[str]:
        """List all templates in a category"""
        pass
