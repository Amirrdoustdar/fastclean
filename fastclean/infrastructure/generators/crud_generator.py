from pathlib import Path
from typing import Dict, Any, List
from .base_generator import BaseGenerator


class CRUDGenerator(BaseGenerator):
    """Generate CRUD operations for an entity"""
    
    def generate_files(self, output_path: Path, context: dict[str, Any]) -> list[Path]:
        """Generate CRUD files"""
        files = []
        
        # Entity
        files.append(self._generate_entity(output_path, context))
        
        # Repository interface
        files.append(self._generate_repository_interface(output_path, context))
        
        # Repository implementation
        files.append(self._generate_repository_impl(output_path, context))
        
        # SQLAlchemy model
        files.append(self._generate_model(output_path, context))
        
        # Use cases
        files.extend(self._generate_use_cases(output_path, context))
        
        # API routes
        files.append(self._generate_routes(output_path, context))
        
        # Schemas
        files.append(self._generate_schemas(output_path, context))
        
        # Dependencies
        files.append(self._generate_dependencies(output_path, context))
        
        return files
    
    def _generate_entity(self, output_path: Path, context: dict[str, Any]) -> Path:
        content = self._render_template("entity", "crud", context)
        path = (
            output_path / "src" / "domain" / "entities" 
            / f"{context['entity_name_snake']}.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_repository_interface(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> Path:
        content = self._render_template("repository_interface", "crud", context)
        path = (
            output_path / "src" / "domain" / "repositories"
            / f"{context['entity_name_snake']}_repository.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_repository_impl(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> Path:
        content = self._render_template("repository_impl", "crud", context)
        path = (
            output_path / "src" / "infrastructure" / "database" / "repositories"
            / f"{context['entity_name_snake']}_repository.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_model(self, output_path: Path, context: dict[str, Any]) -> Path:
        content = self._render_template("model", "crud", context)
        path = (
            output_path / "src" / "infrastructure" / "database" / "models"
            / f"{context['entity_name_snake']}_model.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_use_cases(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> list[Path]:
        files = []
        use_cases = ["create", "get", "update", "delete", "list"]
        
        uc_dir = (
            output_path / "src" / "application" / "usecases"
            / context['entity_name_snake']
        )
        self._file_system.create_directory(uc_dir)
        self._file_system.create_file(uc_dir / "__init__.py", "")
        
        for uc in use_cases:
            content = self._render_template(f"usecase_{uc}", "crud", context)
            path = uc_dir / f"{uc}_{context['entity_name_snake']}.py"
            self._file_system.create_file(path, content)
            files.append(path)
        
        return files
    
    def _generate_routes(self, output_path: Path, context: dict[str, Any]) -> Path:
        content = self._render_template("routes", "crud", context)
        path = (
            output_path / "src" / "interfaces" / "api" / "v1" / "routes"
            / f"{context['entity_name_snake']}.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_schemas(self, output_path: Path, context: dict[str, Any]) -> Path:
        content = self._render_template("schemas", "crud", context)
        path = (
            output_path / "src" / "interfaces" / "schemas"
            / f"{context['entity_name_snake']}.py"
        )
        self._file_system.create_file(path, content)
        return path
    
    def _generate_dependencies(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> Path:
        content = self._render_template("dependencies", "crud", context)
        path = output_path / "src" / "interfaces" / "api" / "dependencies.py"
        
        # Append to existing file if it exists
        if self._file_system.file_exists(path):
            existing = self._file_system.read_file(path)
            content = existing + "\n\n" + content
        
        self._file_system.create_file(path, content)
        return path