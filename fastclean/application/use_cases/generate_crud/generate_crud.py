from pathlib import Path
from typing import List
from fastclean.core.use_case import BaseUseCase
from .dto import GenerateCRUDRequest, GenerateCRUDResponse, FieldDefinition
from fastclean.application.interfaces.file_system import IFileSystemService
from fastclean.application.interfaces.template_engine import ITemplateEngine
from fastclean.core.exceptions.validation import InvalidPathException, InvalidProjectNameException
from fastclean.core.exceptions.base import ValidationException


class GenerateCRUDUseCase(BaseUseCase[GenerateCRUDRequest, GenerateCRUDResponse]):
    """Use case for generating CRUD operations"""
    
    def __init__(
        self,
        file_system: IFileSystemService,
        template_engine: ITemplateEngine
    ):
        self._file_system = file_system
        self._template_engine = template_engine
    
    def execute(self, request: GenerateCRUDRequest) -> GenerateCRUDResponse:
        """Execute CRUD generation"""
        
        # Validate
        self.validate_input(request)
        
        # Generate files
        files_created = []
        context = self._build_context(request)
        
        # Generate entity
        entity_path = self._generate_entity(request, context)
        files_created.append(entity_path)
        
        # Generate repository interface
        repo_interface_path = self._generate_repository_interface(request, context)
        files_created.append(repo_interface_path)
        
        # Generate repository implementation
        repo_impl_path = self._generate_repository_implementation(request, context)
        files_created.append(repo_impl_path)
        
        # Generate use cases
        usecase_paths = self._generate_use_cases(request, context)
        files_created.extend(usecase_paths)
        
        # Generate API routes
        route_path = self._generate_api_routes(request, context)
        files_created.append(route_path)
        
        # Generate schemas
        schema_path = self._generate_schemas(request, context)
        files_created.append(schema_path)
        
        # Generate tests if requested
        if request.generate_tests:
            test_paths = self._generate_tests(request, context)
            files_created.extend(test_paths)
        
        return GenerateCRUDResponse(
            entity_name=request.entity_name,
            files_created=files_created,
            success=True,
            message=f"CRUD for '{request.entity_name}' generated successfully!"
        )
    
    def validate_input(self, request: GenerateCRUDRequest) -> None:
        """Validate input"""
        if not self._file_system.directory_exists(request.project_path):
            raise InvalidPathException(str(request.project_path))
        
        if not request.entity_name.isidentifier():
            raise InvalidProjectNameException(request.entity_name)
        
        if not request.fields:
            raise ValidationException("At least one field is required")
    
    def _build_context(self, request: GenerateCRUDRequest) -> dict:
        """Build template context"""
        return {
            "entity_name": request.entity_name,
            "entity_name_lower": request.entity_name.lower(),
            "entity_name_snake": self._to_snake_case(request.entity_name),
            "fields": request.fields,
            "has_tests": request.generate_tests
        }
    
    def _generate_entity(self, request: GenerateCRUDRequest, context: dict) -> Path:
        """Generate entity file"""
        template = self._template_engine.load_template("entity", "crud")
        content = self._template_engine.render(template, context)
        
        path = (
            request.project_path / "src" / "domain" / "entities" 
            / f"{context['entity_name_snake']}.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_repository_interface(
        self, 
        request: GenerateCRUDRequest, 
        context: dict
    ) -> Path:
        """Generate repository interface"""
        template = self._template_engine.load_template("repository_interface", "crud")
        content = self._template_engine.render(template, context)
        
        path = (
            request.project_path / "src" / "domain" / "repositories" 
            / f"{context['entity_name_snake']}_repository.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_repository_implementation(
        self,
        request: GenerateCRUDRequest,
        context: dict
    ) -> Path:
        """Generate repository implementation"""
        template = self._template_engine.load_template("repository_impl", "crud")
        content = self._template_engine.render(template, context)
        
        path = (
            request.project_path / "src" / "infrastructure" / "database" 
            / "repositories" / f"{context['entity_name_snake']}_repository.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_use_cases(
        self,
        request: GenerateCRUDRequest,
        context: dict
    ) -> list:
        """Generate use case files"""
        paths = []
        use_cases = ["create", "get", "update", "delete", "list"]
        
        usecase_dir = (
            request.project_path / "src" / "application" / "usecases" 
            / context['entity_name_snake']
        )
        self._file_system.create_directory(usecase_dir)
        
        for uc in use_cases:
            template = self._template_engine.load_template(f"usecase_{uc}", "crud")
            content = self._template_engine.render(template, context)
            
            path = usecase_dir / f"{uc}_{context['entity_name_snake']}.py"
            self._file_system.create_file(path, content)
            paths.append(path)
        
        return paths
    
    def _generate_api_routes(
        self,
        request: GenerateCRUDRequest,
        context: dict
    ) -> Path:
        """Generate API routes"""
        template = self._template_engine.load_template("routes", "crud")
        content = self._template_engine.render(template, context)
        
        path = (
            request.project_path / "src" / "interfaces" / "api" / "v1" 
            / "routes" / f"{context['entity_name_snake']}.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_schemas(
        self,
        request: GenerateCRUDRequest,
        context: dict
    ) -> Path:
        """Generate Pydantic schemas"""
        template = self._template_engine.load_template("schemas", "crud")
        content = self._template_engine.render(template, context)
        
        path = (
            request.project_path / "src" / "interfaces" / "schemas" 
            / f"{context['entity_name_snake']}.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_tests(
        self,
        request: GenerateCRUDRequest,
        context: dict
    ) -> list:
        """Generate test files"""
        paths = []
        
        # Unit test
        unit_template = self._template_engine.load_template("test_unit", "crud")
        unit_content = self._template_engine.render(unit_template, context)
        unit_path = (
            request.project_path / "tests" / "unit" 
            / f"test_{context['entity_name_snake']}_usecase.py"
        )
        self._file_system.create_file(unit_path, unit_content)
        paths.append(unit_path)
        
        # Integration test
        int_template = self._template_engine.load_template("test_integration", "crud")
        int_content = self._template_engine.render(int_template, context)
        int_path = (
            request.project_path / "tests" / "integration" 
            / f"test_{context['entity_name_snake']}_api.py"
        )
        self._file_system.create_file(int_path, int_content)
        paths.append(int_path)
        
        return paths
    
    @staticmethod
    def _to_snake_case(text: str) -> str:
        """Convert text to snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()