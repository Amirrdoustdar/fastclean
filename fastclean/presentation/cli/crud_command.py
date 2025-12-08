from pathlib import Path
from typing import Any, Dict, List
from .base import BaseCommand
from ...application.use_cases.generate_crud.generate_crud import GenerateCRUDUseCase
from ...application.use_cases.generate_crud.dto import (
    GenerateCRUDRequest,
    GenerateCRUDResponse,
    FieldDefinition
)
from ...core.exceptions.base import DomainException
from ..formatters.progress_bar import ProgressBar


class CRUDCommand(BaseCommand):
    """Generate CRUD operations for an entity"""
    
    def __init__(
        self,
        generate_crud_usecase: GenerateCRUDUseCase,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._generate_crud = generate_crud_usecase
    
    def execute(self, args: dict[str, Any]) -> int:
        """Execute CRUD generation"""
        try:
            self.print_info(f"🔧 Generating CRUD for: {args['entity']}")
            
            # Parse fields
            fields = self._parse_fields(args.get('fields', ''))
            
            # Create request
            request = GenerateCRUDRequest(
                entity_name=args['entity'],
                project_path=Path(args.get('path', '.')),
                fields=fields,
                generate_tests=args.get('tests', True)
            )
            
            # Execute with progress
            with ProgressBar("Generating CRUD files...") as progress:
                response = self._generate_crud.execute(request)
                progress.complete()
            
            # Display results
            self._display_results(response)
            
            return 0
        
        except DomainException as e:
            self.print_error(f"❌ Error: {e.message}")
            return 1
        
        except Exception as e:
            self.print_error(f"❌ Unexpected error: {str(e)}")
            return 1
    
    def _parse_fields(self, fields_str: str) -> list[FieldDefinition]:
        """Parse fields from string format"""
        if not fields_str:
            return []
        
        fields = []
        for field_def in fields_str.split(','):
            field_def = field_def.strip()
            if ':' in field_def:
                name, type_str = field_def.split(':', 1)
                fields.append(FieldDefinition(
                    name=name.strip(),
                    type=type_str.strip()
                ))
        
        return fields
    
    def _display_results(self, response: GenerateCRUDResponse) -> None:
        """Display generation results"""
        self.print_success(f"\n✅ {response.message}")
        self.print_info(f"\n📝 Files created:")
        for file_path in response.files_created:
            self.print_info(f"   ✓ {file_path}")