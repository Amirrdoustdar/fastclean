from typing import Optional
from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository


class GetUserUseCase:
    """Use case for getting user"""
    
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository
    
    async def execute(self, user_id: int) -> Optional[User]:
        """Execute use case"""
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user