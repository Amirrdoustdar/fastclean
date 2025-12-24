class DomainException(Exception):
    """Base exception for domain errors"""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class ValidationException(DomainException):
    """Exception for validation errors"""


class EntityNotFoundException(DomainException):
    """Exception when entity is not found"""


class DuplicateEntityException(DomainException):
    """Exception when entity already exists"""
