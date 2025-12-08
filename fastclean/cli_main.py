#!/usr/bin/env python3
"""
FastAPI Clean Architecture CLI - Main Entry Point
"""
import sys
import argparse
from pathlib import Path

from fastclean.presentation.cli.init_command import InitCommand
from fastclean.presentation.cli.crud_command import CRUDCommand
from fastclean.presentation.formatters.console_formatter import ConsoleFormatter
from fastclean.infrastructure.file_system.local_file_system import LocalFileSystemService
from fastclean.infrastructure.templates.jinja_engine import JinjaTemplateEngine
from fastclean.infrastructure.validators.project_validator import ProjectValidator
from fastclean.application.use_cases.create_project.create_project import CreateProjectUseCase
from fastclean.application.use_cases.generate_crud.generate_crud import GenerateCRUDUseCase


class DependencyContainer:
    """Dependency Injection Container"""
    
    def __init__(self):
        self.file_system = LocalFileSystemService()
        templates_dir = Path(__file__).parent / "templates"
        self.template_engine = JinjaTemplateEngine(templates_dir)
        self.validator = ProjectValidator()
        
        self.create_project_usecase = CreateProjectUseCase(
            self.file_system,
            self.template_engine,
            self.validator
        )
        
        self.generate_crud_usecase = GenerateCRUDUseCase(
            self.file_system,
            self.template_engine
        )
        
        self.formatter = ConsoleFormatter()
        
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
        prog="fastclean",
        description="FastAPI Clean Architecture CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fastclean init --name=my_project --db=postgresql --docker
  fastclean crud Product --fields="name:str,price:float"
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
        # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new project")
    init_parser.add_argument("--name", required=True, help="Project name")
    init_parser.add_argument("--path", default=".", help="Project path")
    
    # Database
    init_parser.add_argument("--db", default="postgresql", 
                           choices=["postgresql", "mysql", "sqlite", "mongodb"],
                           help="Database type")
    
    # Auth & Cache
    init_parser.add_argument("--auth", default="none",
                           choices=["none", "jwt", "oauth2"],
                           help="Authentication type")
    init_parser.add_argument("--cache", default="none",
                           choices=["none", "redis", "memcached"],
                           help="Cache type")
                           
    # New Features 🚀
    init_parser.add_argument("--queue", default="none",
                           choices=["none", "celery", "arq"],
                           help="Queue system")
    init_parser.add_argument("--storage", default="local",
                           choices=["local", "s3", "minio"],
                           help="File storage")
    init_parser.add_argument("--monitoring", default="none",
                           choices=["none", "prometheus", "sentry"],
                           help="Monitoring tool")
    init_parser.add_argument("--ci", default="none",
                           choices=["none", "github-actions", "gitlab-ci"],
                           help="CI/CD pipeline")
                           
    init_parser.add_argument("--docker", action="store_true", help="Include Docker files")
    init_parser.add_argument("--testing", default="basic", choices=["basic", "full"], help="Testing scope")
    
    # CRUD command
    crud_parser = subparsers.add_parser("crud", help="Generate CRUD operations")
    crud_parser.add_argument("entity", help="Entity name")
    crud_parser.add_argument("--fields", required=True, help='Fields')
    crud_parser.add_argument("--path", default=".", help="Project path")
    crud_parser.add_argument("--no-tests", dest="tests", action="store_false",
                           help="Skip test generation")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    container = DependencyContainer()
    
    try:
        if args.command == "init":
            return container.init_command.execute(vars(args))
        elif args.command == "crud":
            return container.crud_command.execute(vars(args))
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
