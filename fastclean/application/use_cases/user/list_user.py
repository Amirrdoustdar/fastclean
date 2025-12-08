from typing import List
from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository


class ListUsersUseCase:
    """Use case for listing users"""
    
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Execute use case"""
        return await self._repository.get_all(skip=skip, limit=limit)