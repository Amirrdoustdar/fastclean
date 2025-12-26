from datetime import datetime
from typing import Optional
from uuid import uuid4


class BaseEntity:
    """Base entity with common attributes"""

    def __init__(self, id: Optional[str] = None, created_at: Optional[datetime] = None):
        self.id = id or str(uuid4())
        self.created_at = created_at or datetime.now()
