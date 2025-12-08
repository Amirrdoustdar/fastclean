from dataclasses import dataclass, field
from typing import List
from .database_type import DatabaseType
from .auth_type import AuthType
from .cache_type import CacheType


@dataclass(frozen=True)
class ProjectConfig:
    """Immutable project configuration"""
    
    # Core settings
    database: DatabaseType = DatabaseType.POSTGRESQL
    auth: AuthType = AuthType.NONE
    cache: CacheType = CacheType.NONE
    
    # New Features
    queue: str = "none"
    storage: str = "local"
    monitoring: str = "none"
    ci: str = "none"
    
    # Booleans & Versions
    include_docker: bool = False
    include_tests: bool = True
    api_version: str = "v1"
    python_version: str = "3.11"
    
    def get_all_packages(self) -> List[str]:
        """Get all required packages for this configuration"""
        base_packages = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "pydantic-settings==2.1.0",
        ]
        
        packages = base_packages.copy()
        packages.extend(self.database.get_driver_packages())
        packages.extend(self.auth.get_required_packages())
        packages.extend(self.cache.get_required_packages())
        
        # Queue packages
        if self.queue == "celery":
            packages.append("celery==5.3.6")
            packages.append("redis==5.0.1") # Celery needs a broker
            
        # Storage packages
        if self.storage in ["s3", "minio"]:
            packages.append("boto3==1.29.6")
            
        # Monitoring packages
        if self.monitoring == "prometheus":
            packages.append("prometheus-client==0.19.0")
        
        # Testing packages
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
