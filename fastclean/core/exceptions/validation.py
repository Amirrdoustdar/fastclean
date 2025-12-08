from fastclean.core.exceptions.base import (
    ValidationException,
    DuplicateEntityException,
    EntityNotFoundException
)


class InvalidProjectNameException(ValidationException):
    """Exception for invalid project name"""
    
    def __init__(self, name: str):
        super().__init__(
            f"Invalid project name: '{name}'. Must be a valid Python identifier.",
            code="INVALID_PROJECT_NAME"
        )


class InvalidPathException(ValidationException):
    """Exception for invalid path"""
    
    def __init__(self, path: str):
        super().__init__(
            f"Invalid path: '{path}'",
            code="INVALID_PATH"
        )


class ProjectAlreadyExistsException(DuplicateEntityException):
    """Exception when project already exists"""
    
    def __init__(self, project_name: str, path: str):
        super().__init__(
            f"Project '{project_name}' already exists at '{path}'",
            code="PROJECT_EXISTS"
        )


class TemplateNotFoundException(EntityNotFoundException):
    """Exception when template is not found"""
    
    def __init__(self, template_name: str):
        super().__init__(
            f"Template '{template_name}' not found",
            code="TEMPLATE_NOT_FOUND"
        )