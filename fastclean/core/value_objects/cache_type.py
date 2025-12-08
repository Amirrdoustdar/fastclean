from enum import Enum
from typing import List


class CacheType(str, Enum):
    """Cache type enumeration"""
    
    NONE = "none"
    REDIS = "redis"
    MEMCACHED = "memcached"
    IN_MEMORY = "in_memory"
    
    def get_required_packages(self) -> list[str]:
        """Get required packages for this cache type"""
        packages = {
            CacheType.NONE: [],
            CacheType.REDIS: ["redis", "aioredis"],
            CacheType.MEMCACHED: ["aiomcache"],
            CacheType.IN_MEMORY: []
        }
        return packages[self]
    
    def get_default_connection_string(self) -> str:
        """Get default connection string"""
        connections = {
            CacheType.REDIS: "redis://localhost:6379/0",
            CacheType.MEMCACHED: "localhost:11211",
            CacheType.IN_MEMORY: "",
            CacheType.NONE: ""
        }
        return connections[self]