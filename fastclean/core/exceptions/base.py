from typing import Optional


class DomainException(Exception):
    """Base exception for domain errors"""
    
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class ValidationException(DomainException):
    """Exception for validation errors"""
    pass


class EntityNotFoundException(DomainException):
    """Exception when entity is not found"""
    pass


class DuplicateEntityException(DomainException):
    """Exception when entity already exists"""
    pass