from dataclasses import dataclass, field
from typing import Optional, List
from .database_type import DatabaseType
from .auth_type import AuthType
from .cache_type import CacheType


@dataclass(frozen=True)
class ProjectConfig:
    """Immutable project configuration"""
    
    database: DatabaseType = DatabaseType.POSTGRESQL
    auth: AuthType = AuthType.NONE
    cache: CacheType = CacheType.NONE
    include_docker: bool = False
    include_tests: bool = True
    include_ci: bool = False
    api_version: str = "v1"
    python_version: str = "3.11"
    additional_features: List[str] = field(default_factory=list)
    
    def get_all_packages(self) -> List[str]:
        """Get all required packages for this configuration"""
        base_packages = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "pydantic-settings==2.1.0",
            "sqlalchemy[asyncio]==2.0.23"
        ]
        
        packages = base_packages.copy()
        packages.extend(self.database.get_driver_packages())
        packages.extend(self.auth.get_required_packages())
        packages.extend(self.cache.get_required_packages())
        
        if self.include_tests:
            packages.extend([
                "pytest==7.4.3",
                "pytest-asyncio==0.21.1",
                "httpx==0.25.2"
            ])
        
        return packages
    
    def requires_user_entity(self) -> bool:
        """Check if configuration requires User entity"""
        return self.auth.requires_user_model()