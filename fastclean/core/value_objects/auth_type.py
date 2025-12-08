from enum import Enum
from typing import List


class AuthType(str, Enum):
    """Authentication type enumeration"""
    
    NONE = "none"
    JWT = "jwt"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BASIC = "basic"
    
    def get_required_packages(self) -> list[str]:
        """Get required packages for this auth type"""
        packages = {
            AuthType.NONE: [],
            AuthType.JWT: ["python-jose[cryptography]", "passlib[bcrypt]"],
            AuthType.OAUTH2: ["authlib", "httpx"],
            AuthType.API_KEY: [],
            AuthType.BASIC: ["passlib[bcrypt]"]
        }
        return packages[self]
    
    def requires_user_model(self) -> bool:
        """Check if this auth type requires a User model"""
        return self in [AuthType.JWT, AuthType.OAUTH2, AuthType.BASIC]
