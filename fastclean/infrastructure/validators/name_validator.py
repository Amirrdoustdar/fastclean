import re
from typing import List


class NameValidator:
    """Utility class for name validation"""
    
    @staticmethod
    def is_valid_identifier(name: str) -> bool:
        """Check if name is valid Python identifier"""
        return name.isidentifier()
    
    @staticmethod
    def is_snake_case(name: str) -> bool:
        """Check if name is in snake_case"""
        pattern = r'^[a-z][a-z0-9_]*$'
        return bool(re.match(pattern, name))
    
    @staticmethod
    def is_pascal_case(name: str) -> bool:
        """Check if name is in PascalCase"""
        pattern = r'^[A-Z][a-zA-Z0-9]*$'
        return bool(re.match(pattern, name))
    
    @staticmethod
    def is_camel_case(name: str) -> bool:
        """Check if name is in camelCase"""
        pattern = r'^[a-z][a-zA-Z0-9]*$'
        return bool(re.match(pattern, name))
    
    @staticmethod
    def suggest_valid_name(name: str) -> str:
        """Suggest a valid Python identifier from given name"""
        # Remove special characters
        clean = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        # Ensure it doesn't start with a number
        if clean and clean[0].isdigit():
            clean = f"_{clean}"
        
        # Convert to lowercase for snake_case
        return clean.lower() if clean else "project"
