from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class CLISettings(BaseSettings):
    """CLI application settings"""
    
    # Paths
    templates_dir: Optional[Path] = None
    output_dir: Path = Path.cwd()
    
    # Behavior
    verbose: bool = False
    use_colors: bool = True
    
    # Defaults
    default_python_version: str = "3.11"
    default_api_version: str = "v1"
    
    class Config:
        env_prefix = "FASTAPI_CLEAN_"
        env_file = ".env"
