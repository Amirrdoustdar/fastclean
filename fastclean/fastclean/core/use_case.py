from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class BaseUseCase(ABC, Generic[InputDTO, OutputDTO]):
    """Base class for all use cases"""

    @abstractmethod
    def execute(self, request: InputDTO) -> OutputDTO:
        """Execute the use case"""
