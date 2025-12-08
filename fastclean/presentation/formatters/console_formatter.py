from typing import Optional
import sys


class ConsoleFormatter:
    """Format console output with colors"""
    
    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
    }
    
    def __init__(self, use_colors: bool = True):
        self._use_colors = use_colors and sys.stdout.isatty()
    
    def success(self, message: str) -> None:
        """Print success message"""
        self._print(message, 'green')
    
    def error(self, message: str) -> None:
        """Print error message"""
        self._print(message, 'red')
    
    def warning(self, message: str) -> None:
        """Print warning message"""
        self._print(message, 'yellow')
    
    def info(self, message: str) -> None:
        """Print info message"""
        self._print(message, 'cyan')
    
    def bold(self, message: str) -> None:
        """Print bold message"""
        self._print(message, 'bold')
    
    def _print(self, message: str, color: str) -> None:
        """Print colored message"""
        if self._use_colors and color in self.COLORS:
            colored_message = (
                f"{self.COLORS[color]}{message}{self.COLORS['reset']}"
            )
            print(colored_message)
        else:
            print(message)
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Colorize text"""
        if color in ConsoleFormatter.COLORS:
            return (
                f"{ConsoleFormatter.COLORS[color]}{text}"
                f"{ConsoleFormatter.COLORS['reset']}"
            )
        return text