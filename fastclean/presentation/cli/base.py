from abc import ABC, abstractmethod
from typing import Any, Dict
from ..formatters.console_formatter import ConsoleFormatter


class BaseCommand(ABC):
    """Base class for CLI commands"""
    
    def __init__(self, formatter: ConsoleFormatter = None):
        self._formatter = formatter or ConsoleFormatter()
    
    @abstractmethod
    def execute(self, args: dict[str, Any]) -> int:
        """Execute the command"""
        pass
    
    def print_success(self, message: str) -> None:
        """Print success message"""
        self._formatter.success(message)
    
    def print_error(self, message: str) -> None:
        """Print error message"""
        self._formatter.error(message)
    
    def print_info(self, message: str) -> None:
        """Print info message"""
        self._formatter.info(message)
    
    def print_warning(self, message: str) -> None:
        """Print warning message"""
        self._formatter.warning(message)