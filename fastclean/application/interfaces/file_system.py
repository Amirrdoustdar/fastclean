from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class IFileSystemService(ABC):
    """Interface for file system operations"""
    
    @abstractmethod
    def create_directory(self, path: Path) -> None:
        """Create a directory"""
        pass
    
    @abstractmethod
    def create_file(self, path: Path, content: str) -> None:
        """Create a file with content"""
        pass
    
    @abstractmethod
    def directory_exists(self, path: Path) -> bool:
        """Check if directory exists"""
        pass
    
    @abstractmethod
    def file_exists(self, path: Path) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    def read_file(self, path: Path) -> str:
        """Read file content"""
        pass
    
    @abstractmethod
    def list_files(self, path: Path, pattern: str = "*") -> list[Path]:
        """List files in directory"""
        pass