from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastclean.infrastructure.database.database import get_db
from fastclean.infrastructure.database.repositories.user_repository import UserRepository
from ...application.use_cases.user.create_user import CreateUserUseCase
from ..application.use_cases.user.get_user import GetUserUseCase
from ..application.use_cases.user.list_users import ListUsersUseCase

def get_user_repository(session: AsyncSession = Depends(get_db)):
    return UserRepository(session)

def get_create_user_usecase(repo: UserRepository = Depends(get_user_repository)):
    return CreateUserUseCase(repo)

def get_get_user_usecase(repo: UserRepository = Depends(get_user_repository)):
    return GetUserUseCase(repo)

def get_list_users_usecase(repo: UserRepository = Depends(get_user_repository)):
    return ListUsersUseCase(repo)