from pathlib import Path
import fastclean

class PathResolver:
    """Helper to resolve paths relative to the package"""
    
    @staticmethod
    def get_package_root() -> Path:
        """Get the root directory of the installed package"""
        return Path(fastclean.__file__).parent

    @staticmethod
    def get_templates_dir() -> Path:
        """Get the templates directory"""
        return PathResolver.get_package_root() / "templates"