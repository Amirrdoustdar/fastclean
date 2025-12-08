from pathlib import Path
from typing import List
import os
import shutil
from ...application.interfaces.file_system import IFileSystemService


class LocalFileSystemService(IFileSystemService):
    """Local file system implementation"""
    
    def create_directory(self, path: Path) -> None:
        """Create a directory"""
        path.mkdir(parents=True, exist_ok=True)
    
    def create_file(self, path: Path, content: str) -> None:
        """Create a file with content"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    
    def directory_exists(self, path: Path) -> bool:
        """Check if directory exists"""
        return path.exists() and path.is_dir()
    
    def file_exists(self, path: Path) -> bool:
        """Check if file exists"""
        return path.exists() and path.is_file()
    
    def read_file(self, path: Path) -> str:
        """Read file content"""
        return path.read_text(encoding="utf-8")
    
    def list_files(self, path: Path, pattern: str = "*") -> list[Path]:
        """List files in directory"""
        if not self.directory_exists(path):
            return []
        return list(path.glob(pattern))
    
    def copy_file(self, source: Path, destination: Path) -> None:
        """Copy file from source to destination"""
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    
    def delete_directory(self, path: Path) -> None:
        """Delete directory and its contents"""
        if self.directory_exists(path):
            shutil.rmtree(path)