from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ....schemas.user import UserCreate, UserResponse, UserUpdate
from ....api.dependencies import get_create_user_usecase, get_get_user_usecase, get_list_users_usecase
from .....application.usecases.user.create_user import CreateUserUseCase
from .....application.usecases.user.get_user import GetUserUseCase
from .....application.usecases.user.list_users import ListUsersUseCase

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, usecase: CreateUserUseCase = Depends(get_create_user_usecase)):
    try:
        user = await usecase.execute(data.email, data.username)
        return UserResponse(id=user.id, email=user.email, username=user.username,
                          is_active=user.is_active, created_at=user.created_at)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, usecase: GetUserUseCase = Depends(get_get_user_usecase)):
    try:
        user = await usecase.execute(user_id)
        return UserResponse(id=user.id, email=user.email, username=user.username,
                          is_active=user.is_active, created_at=user.created_at)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, 
                    usecase: ListUsersUseCase = Depends(get_list_users_usecase)):
    users = await usecase.execute(skip=skip, limit=limit)
    return [UserResponse(id=u.id, email=u.email, username=u.username,
                        is_active=u.is_active, created_at=u.created_at) for u in users]

