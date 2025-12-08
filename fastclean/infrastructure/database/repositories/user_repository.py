from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository
from ..models.user_model import UserModel


class UserRepository(IUserRepository):
    """SQLAlchemy User Repository"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    def _to_entity(self, model: UserModel) -> User:
        """Convert model to entity"""
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            is_active=model.is_active,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: User) -> UserModel:
        """Convert entity to model"""
        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            is_active=entity.is_active,
            created_at=entity.created_at
        )
    
    async def create(self, user: User) -> User:
        """Create user"""
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users"""
        result = await self._session.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def update(self, user: User) -> User:
        """Update user"""
        model = await self._session.get(UserModel, user.id)
        if not model:
            raise ValueError(f"User {user.id} not found")
        
        model.email = user.email
        model.username = user.username
        model.is_active = user.is_active
        
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)
    
    async def delete(self, user_id: int) -> bool:
        """Delete user"""
        model = await self._session.get(UserModel, user_id)
        if not model:
            return False
        
        await self._session.delete(model)
        return True