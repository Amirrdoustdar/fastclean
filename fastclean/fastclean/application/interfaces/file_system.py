from abc import ABC, abstractmethod
from pathlib import Path


class IFileSystemService(ABC):
    """Interface for file system operations"""

    @abstractmethod
    def create_directory(self, path: Path) -> None:
        """Create a directory"""

    @abstractmethod
    def create_file(self, path: Path, content: str) -> None:
        """Create a file with content"""

    @abstractmethod
    def directory_exists(self, path: Path) -> bool:
        """Check if directory exists"""

    @abstractmethod
    def file_exists(self, path: Path) -> bool:
        """Check if file exists"""

    @abstractmethod
    def read_file(self, path: Path) -> str:
        """Read file content"""

    @abstractmethod
    def list_files(self, path: Path, pattern: str = "*") -> list[Path]:
        """List files in directory"""
