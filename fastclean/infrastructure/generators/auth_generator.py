from pathlib import Path
from typing import Dict, Any, List
from .base_generator import BaseGenerator


class AuthGenerator(BaseGenerator):
    """Generate authentication setup"""
    
    def generate_files(self, output_path: Path, context: dict[str, Any]) -> list[Path]:
        """Generate auth files"""
        files = []
        auth_type = context.get('auth_type', 'jwt')
        
        if auth_type == 'jwt':
            files.extend(self._generate_jwt_auth(output_path, context))
        elif auth_type == 'oauth2':
            files.extend(self._generate_oauth2_auth(output_path, context))
        elif auth_type == 'api_key':
            files.extend(self._generate_api_key_auth(output_path, context))
        
        return files
    
    def _generate_jwt_auth(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> list[Path]:
        """Generate JWT authentication"""
        files = []
        
        auth_dir = output_path / "src" / "infrastructure" / "auth"
        self._file_system.create_directory(auth_dir)
        
        # JWT handler
        content = self._render_template("jwt_handler", "auth", context)
        path = auth_dir / "jwt_handler.py"
        self._file_system.create_file(path, content)
        files.append(path)
        
        # Password hasher
        content = self._render_template("password_hasher", "auth", context)
        path = auth_dir / "password_hasher.py"
        self._file_system.create_file(path, content)
        files.append(path)
        
        # Auth dependencies
        content = self._render_template("auth_dependencies", "auth", context)
        path = auth_dir / "dependencies.py"
        self._file_system.create_file(path, content)
        files.append(path)
        
        # Auth schemas
        content = self._render_template("auth_schemas", "auth", context)
        path = output_path / "src" / "interfaces" / "schemas" / "auth.py"
        self._file_system.create_file(path, content)
        files.append(path)
        
        # Auth routes
        content = self._render_template("auth_routes", "auth", context)
        path = output_path / "src" / "interfaces" / "api" / "v1" / "routes" / "auth.py"
        self._file_system.create_file(path, content)
        files.append(path)
        
        return files
    
    def _generate_oauth2_auth(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> list[Path]:
        """Generate OAuth2 authentication"""
        # Similar implementation for OAuth2
        return []
    
    def _generate_api_key_auth(
        self,
        output_path: Path,
        context: dict[str, Any]
    ) -> list[Path]:
        """Generate API Key authentication"""
        # Similar implementation for API Key
        return []