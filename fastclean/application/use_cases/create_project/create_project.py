from pathlib import Path
from typing import List
from fastclean.core.use_case import BaseUseCase
from .dto import CreateProjectRequest, CreateProjectResponse
from fastclean.application.interfaces.file_system import IFileSystemService
from fastclean.application.interfaces.template_engine import ITemplateEngine
from fastclean.application.interfaces.validator import IValidator
from fastclean.core.entities.project import Project
from fastclean.core.exceptions.validation import (
    InvalidProjectNameException,
    ProjectAlreadyExistsException,
    InvalidPathException,
    ValidationException
)


class CreateProjectUseCase(BaseUseCase[CreateProjectRequest, CreateProjectResponse]):
    """Use case for creating a new FastAPI project"""
    
    def __init__(
        self,
        file_system: IFileSystemService,
        template_engine: ITemplateEngine,
        validator: IValidator
    ):
        self._file_system = file_system
        self._template_engine = template_engine
        self._validator = validator
    
    def execute(self, request: CreateProjectRequest) -> CreateProjectResponse:
        """Execute project creation"""
        
        # Step 1: Validate
        self.validate_input(request)
        
        # Step 2: Create project entity
        project = Project(
            name=request.name,
            path=request.path,
            config=request.config
        )
        
        # Step 3: Check if project exists
        if self._file_system.directory_exists(project.full_path):
            raise ProjectAlreadyExistsException(
                project.name,
                str(project.full_path)
            )
        
        # Step 4: Create project structure
        files_created = self._create_project_structure(project)
        
        # Step 5: Generate files from templates
        files_created += self._generate_project_files(project)
        
        # Step 6: Return response
        return CreateProjectResponse(
            project_id=project.id,
            project_name=project.name,
            project_path=project.full_path,
            files_created=files_created,
            success=True,
            message=f"Project '{project.name}' created successfully!"
        )
    
    def validate_input(self, request: CreateProjectRequest) -> None:
        """Validate input request"""
        if not self._validator.validate_project_name(request.name):
            raise InvalidProjectNameException(request.name)
        
        if not self._validator.validate_path(request.path):
            raise InvalidPathException(str(request.path))
        
        if not self._validator.validate_config(request.config):
            raise ValidationException("Invalid project configuration")
    
    def _create_project_structure(self, project: Project) -> int:
        """Create directory structure"""
        directories = [
            project.full_path,
            project.full_path / "src",
            project.full_path / "src" / "domain" / "entities",
            project.full_path / "src" / "domain" / "repositories",
            project.full_path / "src" / "domain" / "value_objects",
            project.full_path / "src" / "application" / "interfaces",
            project.full_path / "src" / "application" / "usecases" / "user",
            project.full_path / "src" / "infrastructure" / "config",
            project.full_path / "src" / "infrastructure" / "database" / "models",
            project.full_path / "src" / "infrastructure" / "database" / "repositories",
            project.full_path / "src" / "infrastructure" / "external_services",
            project.full_path / "src" / "infrastructure" / "security",
            project.full_path / "src" / "interfaces" / "api" / "v1" / "routes",
            project.full_path / "src" / "interfaces" / "schemas",
            project.full_path / "tests" / "unit",
            project.full_path / "tests" / "integration",
        ]
        
        for directory in directories:
            self._file_system.create_directory(directory)
            # Create __init__.py
            init_file = directory / "__init__.py"
            self._file_system.create_file(init_file, "")
        
        return len(directories)
    
    def _generate_project_files(self, project: Project) -> int:
        """Generate files from templates"""
        context = self._build_template_context(project)
        files_created = 0
        
        # Base categories always included
        template_categories = ["base", "domain", "application", "infrastructure", "interfaces"]
        
        # Conditional categories
        if project.config.include_docker:
            template_categories.append("docker")
            
        # Add other conditional categories here (e.g. ci, monitoring if they have separate folders)
        
        for category in template_categories:
            templates = self._template_engine.list_templates(category)
            
            for template_name in templates:
                template = self._template_engine.load_template(template_name, category)
                content = self._template_engine.render(template, context)
                
                output_path = project.full_path / template.render_path(context)
                self._file_system.create_file(output_path, content)
                files_created += 1
        
        return files_created
    
    def _build_template_context(self, project: Project) -> dict:
        """Build context for template rendering"""
        return {
            "project_name": project.name,
            "database_type": project.config.database.value,
            "database_url": project.config.database.get_connection_string(),
            "auth_type": project.config.auth.value,
            "cache_type": project.config.cache.value,
            
            # New Features
            "queue": project.config.queue,
            "storage": project.config.storage,
            "monitoring": project.config.monitoring,
            "ci": project.config.ci,
            
            "api_version": project.config.api_version,
            "python_version": project.config.python_version,
            "packages": "\n".join(project.config.get_all_packages()),
            "has_docker": project.config.include_docker,
            "has_tests": project.config.include_tests,
            "has_user_model": project.config.requires_user_entity()
        }
