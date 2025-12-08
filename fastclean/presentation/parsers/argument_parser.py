import argparse
from typing import Dict, Any
from ...core.value_objects.database_type import DatabaseType
from ...core.value_objects.auth_type import AuthType
from ...core.value_objects.cache_type import CacheType


class ArgumentParser:
    """Parse CLI arguments"""
    
    def __init__(self):
        self._parser = self._build_parser()
    
    def parse(self, args=None) -> dict[str, Any]:
        """Parse arguments"""
        parsed = self._parser.parse_args(args)
        return vars(parsed)
    
    def _build_parser(self) -> argparse.ArgumentParser:
        """Build argument parser"""
        parser = argparse.ArgumentParser(
            prog='fastapi-clean',
            description='FastAPI Clean Architecture CLI - Rapid project scaffolding',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_examples()
        )
        
        # Add subcommands
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Init command
        self._add_init_command(subparsers)
        
        # CRUD command
        self._add_crud_command(subparsers)
        
        # Feature command
        self._add_feature_command(subparsers)
        
        return parser
    
    def _add_init_command(self, subparsers) -> None:
        """Add init command"""
        init_parser = subparsers.add_parser(
            'init',
            help='Initialize a new FastAPI project'
        )
        
        init_parser.add_argument(
            '--name',
            type=str,
            required=True,
            help='Project name'
        )
        
        init_parser.add_argument(
            '--path',
            type=str,
            default='.',
            help='Project path (default: current directory)'
        )
        
        init_parser.add_argument(
            '--db',
            type=str,
            choices=[db.value for db in DatabaseType],
            default='postgresql',
            help='Database type (default: postgresql)'
        )
        
        init_parser.add_argument(
            '--auth',
            type=str,
            choices=[auth.value for auth in AuthType],
            default='none',
            help='Authentication type (default: none)'
        )
        
        init_parser.add_argument(
            '--cache',
            type=str,
            choices=[cache.value for cache in CacheType],
            default='none',
            help='Cache type (default: none)'
        )
        
        init_parser.add_argument(
            '--docker',
            action='store_true',
            help='Include Docker files'
        )
        
        init_parser.add_argument(
            '--no-tests',
            dest='tests',
            action='store_false',
            help='Skip test files generation'
        )
        
        init_parser.add_argument(
            '--ci',
            action='store_true',
            help='Include CI/CD configuration'
        )
        
        init_parser.add_argument(
            '--python-version',
            type=str,
            default='3.11',
            help='Python version (default: 3.11)'
        )
    
    def _add_crud_command(self, subparsers) -> None:
        """Add CRUD command"""
        crud_parser = subparsers.add_parser(
            'crud',
            help='Generate CRUD operations for an entity'
        )
        
        crud_parser.add_argument(
            'entity',
            type=str,
            help='Entity name (e.g., Product, Order)'
        )
        
        crud_parser.add_argument(
            '--fields',
            type=str,
            required=True,
            help='Fields definition (e.g., "name:str,price:float,stock:int")'
        )
        
        crud_parser.add_argument(
            '--path',
            type=str,
            default='.',
            help='Project path (default: current directory)'
        )
        
        crud_parser.add_argument(
            '--no-tests',
            dest='tests',
            action='store_false',
            help='Skip test generation'
        )
    
    def _add_feature_command(self, subparsers) -> None:
        """Add feature command"""
        feature_parser = subparsers.add_parser(
            'feature',
            help='Add feature to existing project'
        )
        
        feature_parser.add_argument(
            'feature',
            type=str,
            choices=['auth', 'cache', 'monitoring', 'websocket'],
            help='Feature to add'
        )
        
        feature_parser.add_argument(
            '--path',
            type=str,
            default='.',
            help='Project path (default: current directory)'
        )
        
        feature_parser.add_argument(
            '--type',
            type=str,
            help='Feature type (e.g., jwt for auth, redis for cache)'
        )
    
    @staticmethod
    def _get_examples() -> str:
        """Get usage examples"""
        return """
Examples:
  # Create simple project
  fastapi-clean init --name=myproject
  
  # Create project with PostgreSQL and Docker
  fastapi-clean init --name=myproject --db=postgresql --docker
  
  # Create project with JWT authentication
  fastapi-clean init --name=myproject --auth=jwt --docker
  
  # Generate CRUD for Product entity
  fastapi-clean crud Product --fields="name:str,price:float,stock:int"
  
  # Add authentication to existing project
  fastapi-clean feature auth --type=jwt --path=./myproject
  
  # Add Redis caching
  fastapi-clean feature cache --type=redis --path=./myproject
"""
