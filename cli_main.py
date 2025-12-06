#!/usr/bin/env python3
"""
FastAPI Clean Architecture CLI - Main Entry Point
"""
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from presentation.cli.init_command import InitCommand
from presentation.cli.crud_command import CRUDCommand
from presentation.formatters.console_formatter import ConsoleFormatter
from infrastructure.file_system.local_file_system import LocalFileSystemService
from infrastructure.templates.jinja_engine import JinjaTemplateEngine
from infrastructure.validators.project_validator import ProjectValidator
from application.use_cases.create_project.create_project import CreateProjectUseCase
from application.use_cases.generate_crud.generate_crud import GenerateCRUDUseCase


class DependencyContainer:
    """Dependency Injection Container"""
    
    def __init__(self):
        # Infrastructure
        self.file_system = LocalFileSystemService()
        templates_dir = Path(__file__).parent / "templates"
        self.template_engine = JinjaTemplateEngine(templates_dir)
        self.validator = ProjectValidator()
        
        # Use Cases
        self.create_project_usecase = CreateProjectUseCase(
            self.file_system,
            self.template_engine,
            self.validator
        )
        
        self.generate_crud_usecase = GenerateCRUDUseCase(
            self.file_system,
            self.template_engine
        )
        
        # Presentation
        self.formatter = ConsoleFormatter()
        
        # Commands
        self.init_command = InitCommand(
            self.create_project_usecase,
            formatter=self.formatter
        )
        
        self.crud_command = CRUDCommand(
            self.generate_crud_usecase,
            formatter=self.formatter
        )


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="fastapi-clean",
        description="FastAPI Clean Architecture CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new project
  fastapi-clean init --name=my_project --db=postgresql --docker
  
  # Generate CRUD
  fastapi-clean crud Product --fields="name:str,price:float"
  
  # Add authentication
  fastapi-clean feature auth --type=jwt
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new project")
    init_parser.add_argument("--name", required=True, help="Project name")
    init_parser.add_argument("--path", default=".", help="Project path")
    init_parser.add_argument("--db", default="postgresql", 
                           choices=["postgresql", "mysql", "sqlite", "mongodb"],
                           help="Database type")
    init_parser.add_argument("--auth", default="none",
                           choices=["none", "jwt", "oauth2", "api_key"],
                           help="Authentication type")
    init_parser.add_argument("--cache", default="none",
                           choices=["none", "redis", "memcached"],
                           help="Cache type")
    init_parser.add_argument("--docker", action="store_true",
                           help="Include Docker files")
    init_parser.add_argument("--no-tests", dest="tests", action="store_false",
                           help="Skip test generation")
    
    # CRUD command
    crud_parser = subparsers.add_parser("crud", help="Generate CRUD operations")
    crud_parser.add_argument("entity", help="Entity name (e.g., Product)")
    crud_parser.add_argument("--fields", required=True,
                           help='Fields definition (e.g., "name:str,price:float")')
    crud_parser.add_argument("--path", default=".", help="Project path")
    crud_parser.add_argument("--no-tests", dest="tests", action="store_false",
                           help="Skip test generation")
    
    # Feature command
    feature_parser = subparsers.add_parser("feature", help="Add feature")
    feature_parser.add_argument("feature", 
                              choices=["auth", "cache", "monitoring"],
                              help="Feature to add")
    feature_parser.add_argument("--type", help="Feature type")
    feature_parser.add_argument("--path", default=".", help="Project path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Create container
    container = DependencyContainer()
    
    try:
        if args.command == "init":
            return container.init_command.execute(vars(args))
        elif args.command == "crud":
            return container.crud_command.execute(vars(args))
        elif args.command == "feature":
            print("Feature command coming soon!")
            return 0
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
