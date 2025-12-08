from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader
from fastclean.application.interfaces.template_engine import ITemplateEngine
from fastclean.core.entities.template import Template
from fastclean.core.exceptions.validation import TemplateNotFoundException
from fastclean.infrastructure.file_system.path_resolver import PathResolver


class JinjaTemplateEngine(ITemplateEngine):
    """Jinja2 template engine implementation"""
    
    # Mapping for base files output paths
    PATH_MAPPINGS = {
        # Base Configuration
        "main": "src/main.py",
        "settings": "src/infrastructure/config/settings.py",
        "database": "src/infrastructure/config/database.py",
        "env": ".env",
        "gitignore": ".gitignore",
        "readme": "README.md",
        "requirements": "requirements.txt",
        "dockerfile": "Dockerfile",
        "docker_compose": "docker-compose.yml",
        
        # User Module
        "user_model": "src/infrastructure/database/models/user.py",
        "user_repository_interface": "src/domain/repositories/user_repository.py",
        "user_repository_impl": "src/infrastructure/database/repositories/user_repository.py",
        "user_routes": "src/interfaces/api/v1/routes/user.py",
        "user_schema": "src/interfaces/schemas/user.py",
        "user_entity": "src/domain/entities/user.py",
        
        # New Features 🚀
        "jwt_handler": "src/infrastructure/security/jwt_handler.py",
        "celery_app": "src/infrastructure/worker/celery_app.py",
        "storage_client": "src/infrastructure/external_services/storage.py",
    }
    
    def __init__(self, templates_dir: Path = None):
        self._templates_dir = templates_dir or PathResolver.get_templates_dir()
        self._env = Environment(
            loader=FileSystemLoader(str(self._templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        self._env.filters['snake_case'] = self._to_snake_case
        self._env.filters['camel_case'] = self._to_camel_case
        self._env.filters['pascal_case'] = self._to_pascal_case
    
    def render(self, template: Template, context: dict) -> str:
        jinja_template = self._env.from_string(template.content)
        return jinja_template.render(**context)
    
    def load_template(self, template_name: str, category: str) -> Template:
        possible_names = [
            f"{template_name}.py.j2",
            f"{template_name}.j2",
            f"{template_name}.yml.j2",
            f"{template_name}.md.j2",
            f"{template_name}.txt.j2",
        ]
        
        template_path = None
        for name in possible_names:
            path = self._templates_dir / category / name
            if path.exists():
                template_path = path
                break
        
        # اگر فایل پیدا نشد، خطا ندهیم (چون برخی فیچرها اختیاری هستند)
        if not template_path:
            # اینجا می‌توانیم لاگ کنیم یا Exception خاصی برای هندل کردن بدهیم
            # فعلاً برای جلوگیری از کرش در صورت نبود فایل آپشنال:
            if category in ["infrastructure", "domain"]: # فایل‌های حیاتی
                 raise TemplateNotFoundException(f"{category}/{template_name}")
            return None # برای فایل‌های غیر حیاتی

        content = template_path.read_text(encoding="utf-8")
        variables = self._extract_variables(content)
        
        return Template(
            name=template_name,
            content=content,
            variables=variables,
            category=category,
            output_path=self._determine_output_path(template_name, category)
        )
    
    def list_templates(self, category: str) -> list:
        category_path = self._templates_dir / category
        if not category_path.exists():
            return []
        
        templates = []
        for template_file in category_path.glob("*.j2"):
            template_name = template_file.name.split('.')[0]
            if template_name not in templates:
                templates.append(template_name)
        return templates
    
    def _determine_output_path(self, template_name: str, category: str) -> Path:
        if template_name in self.PATH_MAPPINGS:
            return Path(self.PATH_MAPPINGS[template_name])
        return Path(template_name.replace("_", "/"))

    @staticmethod
    def _extract_variables(content: str) -> dict:
        import re
        pattern = r'\{\{\s*(\w+)\s*\}\}'
        variables = re.findall(pattern, content)
        return {var: "" for var in set(variables)}
    
    @staticmethod
    def _to_snake_case(text: str) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def _to_camel_case(text: str) -> str:
        components = text.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def _to_pascal_case(text: str) -> str:
        return ''.join(x.title() for x in text.split('_'))
