from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository


class CreateUserUseCase:
    """Use case for creating user"""
    
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository
    
    async def execute(self, email: str, username: str) -> User:
        """Execute use case"""
        # Check if user exists
        existing = await self._repository.get_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")
        
        # Create user
        user = User(email=email, username=username)
        return await self._repository.create(user)