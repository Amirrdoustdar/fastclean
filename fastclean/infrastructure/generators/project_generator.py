from pathlib import Path
from typing import Dict, Any, List
from .base_generator import BaseGenerator


class ProjectGenerator(BaseGenerator):
    """Generate complete project structure"""
    
    def prepare(self, output_path: Path, context: dict[str, Any]) -> None:
        """Create base directory structure"""
        directories = [
            "src/domain/entities",
            "src/domain/repositories",
            "src/domain/value_objects",
            "src/application/interfaces",
            "src/application/usecases",
            "src/infrastructure/config",
            "src/infrastructure/database/models",
            "src/infrastructure/database/repositories",
            "src/infrastructure/external_services",
            "src/interfaces/api/v1/routes",
            "src/interfaces/schemas",
            "tests/unit",
            "tests/integration",
        ]
        
        for dir_path in directories:
            full_path = output_path / dir_path
            self._file_system.create_directory(full_path)
            # Create __init__.py
            self._file_system.create_file(full_path / "__init__.py", "")
    
    def generate_files(self, output_path: Path, context: dict[str, Any]) -> list[Path]:
        """Generate all project files"""
        files_created = []
        
        # Main file
        files_created.append(self._generate_main(output_path, context))
        
        # Settings
        files_created.append(self._generate_settings(output_path, context))
        
        # Database setup
        files_created.append(self._generate_database(output_path, context))
        
        # Requirements
        files_created.append(self._generate_requirements(output_path, context))
        
        # Environment file
        files_created.append(self._generate_env(output_path, context))
        
        # Gitignore
        files_created.append(self._generate_gitignore(output_path, context))
        
        # README
        files_created.append(self._generate_readme(output_path, context))
        
        # Docker files (if enabled)
        if context.get('has_docker'):
            files_created.extend(self._generate_docker_files(output_path, context))
        
        return files_created
    
    def _generate_main(self, output_path: Path, context: dict[str, Any]) -> Path:
        """Generate main.py"""
        content = self._render_template("main", "base", context)
        path = output_path / "src" / "main.py"
        self._file_system.create_file(path, content)
        return path
    
    def _generate_settings(self, output_path: Path, context: dict[str, Any]) -> Path:
        """Generate settings.py"""
        content = self._render_template("settings", "base", context)
        path = output_path / "src" / "infrastructure" / "config" / "settings.py"
        self._file_system.create_file(path, content)
        return path
    
    def _generate_database(self, output_path: Path, context: dict[str, Any]) -> Path:
        """Generate database.py"""
        content = self._render_template("database", "base", context)
        path = output_path / "src" / "infrastructure" / "database" / "database.py"
        self._file_system.create_file(path, content)
        return path
    
    def _generate_requirements(self, output_path: Path, context: dict[str, Any]) -> Path:
        """Generate requirements.txt"""
        content = context['packages']
        path = output_path / "requirements.txt"
        self._file_system.create_file(path, content)
        return path
    
    def _generate_env(self, output_path: Path, context: dict[str, Any]) -> Path:
        """Generate .env"""
        content = self._render_template("env", "base", context)
        path = output_path / ".env"
        self._file_system.create_file(path, content)
        return path
    
    def _generate_gitignore(self, output_path: Path, context: dict[str, Any]) -> Path:
        """Generate .gitignore"""
        content = self._render_template("gitignore", "base", context)
        path = output_path / ".gitignore"
        self._file_system.create_file(path, content)
        return path
    
    def _generate_readme(self, output_path: Path, context: dict[str, Any]) -> Path:
        """Generate README.md"""
        content = self._render_template("readme", "base", context)
        path = output_path / "README.md"
        self._file_system.create_file(path, content)
        return path
    
    def _generate_docker_files(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> list[Path]:
        """Generate Docker files"""
        files = []
        
        # Dockerfile
        content = self._render_template("dockerfile", "base", context)
        path = output_path / "Dockerfile"
        self._file_system.create_file(path, content)
        files.append(path)
        
        # docker-compose.yml
        content = self._render_template("docker_compose", "base", context)
        path = output_path / "docker-compose.yml"
        self._file_system.create_file(path, content)
        files.append(path)
        
        return files
