import sys
import time
from typing import Optional
import threading


class ProgressBar:
    """Animated progress indicator"""
    
    SPINNER_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    def __init__(self, message: str = "Processing..."):
        self.message = message
        self._stop = False
        self._thread: Optional[threading.Thread] = None
    
    def __enter__(self):
        """Start progress indicator"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop progress indicator"""
        self.stop()
    
    def start(self) -> None:
        """Start the progress animation"""
        self._stop = False
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the progress animation"""
        self._stop = True
        if self._thread:
            self._thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def complete(self) -> None:
        """Mark as complete"""
        self.stop()
    
    def _animate(self) -> None:
        """Animate the spinner"""
        idx = 0
        while not self._stop:
            frame = self.SPINNER_FRAMES[idx % len(self.SPINNER_FRAMES)]
            sys.stdout.write(f'\r{frame} {self.message}')
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1