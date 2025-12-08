from enum import Enum
from typing import Optional, List


class DatabaseType(str, Enum):
    """Database type enumeration"""
    
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    
    def get_connection_string(
        self,
        host: str = "localhost",
        port: Optional[int] = None,
        database: str = "app_db",
        username: str = "user",
        password: str = "password"
    ) -> str:
        """Generate connection string for the database"""
        
        port = port or self.default_port()
        
        if self == DatabaseType.POSTGRESQL:
            return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        
        elif self == DatabaseType.MYSQL:
            return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        
        elif self == DatabaseType.SQLITE:
            return f"sqlite+aiosqlite:///./{database}.db"
        
        elif self == DatabaseType.MONGODB:
            return f"mongodb://{username}:{password}@{host}:{port}/{database}"
        
        raise ValueError(f"Unknown database type: {self}")
    
    def default_port(self) -> int:
        """Get default port for the database"""
        ports = {
            DatabaseType.POSTGRESQL: 5432,
            DatabaseType.MYSQL: 3306,
            DatabaseType.SQLITE: 0,
            DatabaseType.MONGODB: 27017
        }
        return ports[self]
    
    def get_driver_packages(self) -> list[str]:
        """Get required Python packages for this database"""
        packages = {
            DatabaseType.POSTGRESQL: ["asyncpg", "psycopg2-binary"],
            DatabaseType.MYSQL: ["aiomysql", "pymysql"],
            DatabaseType.SQLITE: ["aiosqlite"],
            DatabaseType.MONGODB: ["motor", "pymongo"]
        }
        return packages[self]