from pathlib import Path
from typing import List
from ..base import BaseUseCase
from .dto import AddCachingRequest, AddFeatureResponse
from fastclean.application.interfaces.file_system import IFileSystemService
from fastclean.application.interfaces.template_engine import ITemplateEngine
from fastclean.core.exceptions.validation import InvalidPathException


class AddCachingUseCase(BaseUseCase[AddCachingRequest, AddFeatureResponse]):
    """Use case for adding caching to existing project"""
    
    def __init__(
        self,
        file_system: IFileSystemService,
        template_engine: ITemplateEngine
    ):
        self._file_system = file_system
        self._template_engine = template_engine
    
    def execute(self, request: AddCachingRequest) -> AddFeatureResponse:
        """Execute caching addition"""
        self.validate_input(request)
        
        files_created = []
        files_modified = []
        
        if request.cache_type == 'redis':
            files_created.extend(self._add_redis_cache(request))
        elif request.cache_type == 'memcached':
            files_created.extend(self._add_memcached_cache(request))
        elif request.cache_type == 'in_memory':
            files_created.extend(self._add_in_memory_cache(request))
        
        # Update requirements
        requirements_path = request.project_path / "requirements.txt"
        if self._file_system.file_exists(requirements_path):
            self._update_requirements(requirements_path, request.cache_type)
            files_modified.append(requirements_path)
        
        return AddFeatureResponse(
            feature_name=f"caching_{request.cache_type}",
            files_created=files_created,
            files_modified=files_modified,
            success=True,
            message=f"Successfully added {request.cache_type.upper()} caching!"
        )
    
    def validate_input(self, request: AddCachingRequest) -> None:
        """Validate input"""
        if not self._file_system.directory_exists(request.project_path):
            raise InvalidPathException(str(request.project_path))
        
        valid_types = ['redis', 'memcached', 'in_memory']
        if request.cache_type not in valid_types:
            raise ValueError(f"Cache type must be one of: {', '.join(valid_types)}")
    
    def _add_redis_cache(self, request: AddCachingRequest) -> list[Path]:
        """Add Redis caching"""
        files_created = []
        
        # Create cache directory
        cache_dir = request.project_path / "src" / "infrastructure" / "cache"
        self._file_system.create_directory(cache_dir)
        
        # Redis client
        redis_client_content = '''"""Redis Cache Client"""
import redis.asyncio as redis
from typing import Optional, Any
import json
from ...config.settings import settings

class RedisCache:
    """Redis cache implementation"""
    
    def __init__(self):
        self.redis = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache"""
        await self.redis.setex(key, ttl, json.dumps(value))
    
    async def delete(self, key: str) -> None:
        """Delete key from cache"""
        await self.redis.delete(key)
    
    async def close(self) -> None:
        """Close Redis connection"""
        await self.redis.close()

cache = RedisCache()
'''
        redis_path = cache_dir / "redis_client.py"
        self._file_system.create_file(redis_path, redis_client_content)
        files_created.append(redis_path)
        
        # Cache decorator
        decorator_content = '''"""Cache Decorator"""
from functools import wraps
from typing import Callable
from .redis_client import cache

def cached(ttl: int = 300):
    """Cache decorator"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
'''
        decorator_path = cache_dir / "decorator.py"
        self._file_system.create_file(decorator_path, decorator_content)
        files_created.append(decorator_path)
        
        # Update settings
        self._update_settings_for_redis(request.project_path, request.connection_string)
        
        return files_created
    
    def _add_memcached_cache(self, request: AddCachingRequest) -> list[Path]:
        """Add Memcached caching"""
        # TODO: Implement
        return []
    
    def _add_in_memory_cache(self, request: AddCachingRequest) -> list[Path]:
        """Add in-memory caching"""
        # TODO: Implement
        return []
    
    def _update_requirements(self, requirements_path: Path, cache_type: str) -> None:
        """Update requirements.txt"""
        content = self._file_system.read_file(requirements_path)
        
        packages = []
        if cache_type == 'redis':
            packages = ['redis==5.0.1']
        elif cache_type == 'memcached':
            packages = ['aiomcache==0.8.1']
        
        for package in packages:
            if package.split('==')[0] not in content:
                content += f"\n{package}"
        
        self._file_system.create_file(requirements_path, content)
    
    def _update_settings_for_redis(self, project_path: Path, connection_string: str) -> None:
        """Update settings.py"""
        settings_path = project_path / "src" / "infrastructure" / "config" / "settings.py"
        
        if self._file_system.file_exists(settings_path):
            content = self._file_system.read_file(settings_path)
            
            redis_config = f'''
    # Redis Cache
    REDIS_URL: str = "{connection_string or 'redis://localhost:6379/0'}"
    CACHE_TTL: int = 300
'''
            
            if 'REDIS_URL' not in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'class Config:' in line:
                        lines.insert(i, redis_config)
                        break
                
                content = '\n'.join(lines)
                self._file_system.create_file(settings_path, content)
