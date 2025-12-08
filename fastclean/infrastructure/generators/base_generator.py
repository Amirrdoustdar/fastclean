from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
from ...application.interfaces.file_system import IFileSystemService
from ...application.interfaces.template_engine import ITemplateEngine


class BaseGenerator(ABC):
    """Base class for code generators"""
    
    def __init__(
        self,
        file_system: IFileSystemService,
        template_engine: ITemplateEngine
    ):
        self._file_system = file_system
        self._template_engine = template_engine
    
    def generate(self, output_path: Path, context: dict[str, Any]) -> list[Path]:
        """Template method for generation"""
        # Step 1: Prepare
        self.prepare(output_path, context)
        
        # Step 2: Generate files
        files = self.generate_files(output_path, context)
        
        # Step 3: Post-process
        self.post_process(output_path, context)
        
        return files
    
    def prepare(self, output_path: Path, context: dict[str, Any]) -> None:
        """Prepare for generation (can be overridden)"""
        pass
    
    @abstractmethod
    def generate_files(self, output_path: Path, context: dict[str, Any]) -> list[Path]:
        """Generate files (must be implemented)"""
        pass
    
    def post_process(self, output_path: Path, context: dict[str, Any]) -> None:
        """Post-process after generation (can be overridden)"""
        pass
    
    def _render_template(
        self,
        template_name: str,
        category: str,
        context: dict[str, Any]
    ) -> str:
        """Render a template"""
        template = self._template_engine.load_template(template_name, category)
        return self._template_engine.render(template, context)