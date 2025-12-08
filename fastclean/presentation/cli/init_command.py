from pathlib import Path
from typing import Any
from .base import BaseCommand
from ...application.use_cases.create_project.create_project import CreateProjectUseCase
from ...application.use_cases.create_project.dto import (
    CreateProjectRequest,
    CreateProjectResponse
)
from ...core.value_objects.project_config import ProjectConfig
from ...core.value_objects.database_type import DatabaseType
from ...core.value_objects.auth_type import AuthType
from ...core.value_objects.cache_type import CacheType
from ...core.exceptions.base import DomainException
from ..formatters.progress_bar import ProgressBar


class InitCommand(BaseCommand):
    """Initialize a new FastAPI project"""
    
    def __init__(
        self,
        create_project_usecase: CreateProjectUseCase,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._create_project = create_project_usecase
    
    def execute(self, args: dict[str, Any]) -> int:
        """Execute init command"""
        try:
            # Display start message
            self.print_info(f"🚀 Creating project: {args['name']}")
            
            # Build configuration
            config = self._build_config(args)
            
            # Create request
            request = CreateProjectRequest(
                name=args['name'],
                path=Path(args.get('path', '.')),
                config=config
            )
            
            # Execute with progress
            with ProgressBar("Generating project files...") as progress:
                response = self._create_project.execute(request)
                progress.complete()
            
            # Display results
            self._display_success(response)
            self._display_next_steps(response)
            
            return 0
        
        except DomainException as e:
            self.print_error(f"❌ Error: {e.message}")
            return 1
        
        except Exception as e:
            self.print_error(f"❌ Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return 1
    
    def _build_config(self, args: dict[str, Any]) -> ProjectConfig:
        """Build project configuration from arguments"""
        return ProjectConfig(
            database=DatabaseType(args.get('db', 'postgresql')),
            auth=AuthType(args.get('auth', 'none')),
            cache=CacheType(args.get('cache', 'none')),
            queue=args.get('queue', 'none'),
            storage=args.get('storage', 'local'),
            monitoring=args.get('monitoring', 'none'),
            ci=args.get('ci', 'none'),
            include_docker=args.get('docker', False),
            include_tests=True if args.get('testing') == 'full' else False,
            api_version=args.get('api_version', 'v1'),
            python_version=args.get('python_version', '3.11')
        )
    
    def _display_success(self, response: CreateProjectResponse) -> None:
        """Display success message"""
        self.print_success(f"\n✅ {response.message}")
        self.print_info(f"📁 Location: {response.project_path}")
        self.print_info(f"📝 Files created: {response.files_created}")
    
    def _display_next_steps(self, response: CreateProjectResponse) -> None:
        """Display next steps"""
        self.print_info("\n🔧 Next steps:")
        self.print_info(f"   cd {response.project_name}")
        self.print_info("   python -m venv venv")
        self.print_info("   source venv/bin/activate  # Windows: venv\\Scripts\\activate")
        self.print_info("   pip install -r requirements.txt")
        self.print_info("   uvicorn src.main:app --reload")
        self.print_info("\n📚 Documentation: http://localhost:8000/docs")