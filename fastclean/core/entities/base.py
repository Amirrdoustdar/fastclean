from abc import ABC
from datetime import datetime
from typing import Optional
from uuid import uuid4


class BaseEntity(ABC):
    """Base entity with common attributes"""
    
    def __init__(self, id: Optional[str] = None):
        self._id = id or str(uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def update_timestamp(self) -> None:
        self._updated_at = datetime.now()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)