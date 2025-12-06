from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, Template as JinjaTemplate
from ...application.interfaces.template_engine import ITemplateEngine
from ...core.entities.template import Template
from ...core.exceptions.validation import TemplateNotFoundException
from ..file_system.path_resolver import PathResolver


class JinjaTemplateEngine(ITemplateEngine):
    """Jinja2 template engine implementation"""
    
    def __init__(self, templates_dir: Path = None):
        self._templates_dir = templates_dir or PathResolver.get_templates_dir()
        self._env = Environment(
            loader=FileSystemLoader(str(self._templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # Add custom filters
        self._env.filters['snake_case'] = self._to_snake_case
        self._env.filters['camel_case'] = self._to_camel_case
        self._env.filters['pascal_case'] = self._to_pascal_case
    
    def render(self, template: Template, context: Dict[str, Any]) -> str:
        """Render template with context"""
        jinja_template = self._env.from_string(template.content)
        return jinja_template.render(**context)
    
    def load_template(self, template_name: str, category: str) -> Template:
        """Load template by name and category"""
        template_path = self._templates_dir / category / f"{template_name}.j2"
        
        if not template_path.exists():
            raise TemplateNotFoundException(f"{category}/{template_name}")
        
        content = template_path.read_text(encoding="utf-8")
        variables = self._extract_variables(content)
        
        return Template(
            name=template_name,
            content=content,
            variables=variables,
            category=category,
            output_path=self._determine_output_path(template_name, category)
        )
    
    def list_templates(self, category: str) -> List[str]:
        """List all templates in a category"""
        category_path = self._templates_dir / category
        
        if not category_path.exists():
            return []
        
        templates = []
        for template_file in category_path.glob("*.j2"):
            template_name = template_file.stem
            templates.append(template_name)
        
        return templates
    
    @staticmethod
    def _extract_variables(content: str) -> Dict[str, str]:
        """Extract variables from template content"""
        import re
        pattern = r'\{\{\s*(\w+)\s*\}\}'
        variables = re.findall(pattern, content)
        return {var: "" for var in set(variables)}
    
    @staticmethod
    def _determine_output_path(template_name: str, category: str) -> Path:
        """Determine output path for template"""
        # This can be customized based on template naming conventions
        return Path(template_name.replace("_", "/"))
    
    @staticmethod
    def _to_snake_case(text: str) -> str:
        """Convert to snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def _to_camel_case(text: str) -> str:
        """Convert to camelCase"""
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def _to_pascal_case(text: str) -> str:
        """Convert to PascalCase"""
        return ''.join(x.title() for x in text.split('_'))