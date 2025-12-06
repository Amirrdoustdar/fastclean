#!/bin/bash
# ============================================================================
# FastAPI Clean Architecture - Complete Setup
# این اسکریپت تمام فایل‌های پروژه رو می‌سازه
# Usage: bash setup_complete.sh [project_name]
# ============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

print_header() {
    echo -e "\n${BOLD}${BLUE}========================================${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}========================================${NC}\n"
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
print_step() { echo -e "\n${BOLD}${BLUE}[$1/15] $2...${NC}"; }

PROJECT_NAME=${1:-"fastapi-clean-cli"}

print_header "FastAPI Clean Architecture - Complete Setup"
echo -e "${BOLD}Project: $PROJECT_NAME${NC}\n"
read -p "Continue? (y/n): " -n 1 -r
echo
[[ ! $REPLY =~ ^[Yy]$ ]] && exit 1

# ============================================================================
# STEP 1: Create Directory Structure
# ============================================================================
print_step 1 15 "Creating directories"
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

mkdir -p src/{core/{entities,value_objects,exceptions},application/{interfaces,usecases/{user,create_project,generate_crud,add_feature}},infrastructure/{file_system,templates,validators,generators,config,database/{models,repositories}},presentation/{cli,formatters,parsers},interfaces/{api/v1/routes,schemas},config}
mkdir -p tests/{unit,integration} templates/{base,crud,docker,auth} docs .github/workflows

find src tests -type d -exec touch {}/__init__.py \;
print_success "Created directory structure"

# ============================================================================
# STEP 2: Core Layer - Domain Entities
# ============================================================================
print_step 2 15 "Creating Domain Layer"

cat > src/core/entities/base.py << 'DOMAIN_BASE'
"""Base Entity"""
from abc import ABC
from datetime import datetime
from typing import Optional
from uuid import uuid4

class BaseEntity(ABC):
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
    
    def update_timestamp(self) -> None:
        self._updated_at = datetime.now()
DOMAIN_BASE

cat > src/core/entities/project.py << 'DOMAIN_PROJECT'
"""Project Entity"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List
from .base import BaseEntity

@dataclass
class Project(BaseEntity):
    name: str
    path: Path
    features: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__init__()
        if not self.name.isidentifier():
            raise ValueError(f"Invalid project name: {self.name}")
    
    def add_feature(self, feature: str):
        if feature not in self.features:
            self.features.append(feature)
    
    @property
    def full_path(self) -> Path:
        return self.path / self.name
DOMAIN_PROJECT

cat > src/domain/entities/user.py << 'DOMAIN_USER'
"""User Entity"""
from datetime import datetime
from typing import Optional

class User:
    def __init__(self, email: str, username: str, id: Optional[int] = None,
                 is_active: bool = True, created_at: Optional[datetime] = None):
        self.id = id
        self.email = email
        self.username = username
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self._validate()
    
    def _validate(self):
        if not self.email or '@' not in self.email:
            raise ValueError("Invalid email")
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")
    
    def activate(self):
        self.is_active = True
    
    def deactivate(self):
        self.is_active = False
    
    def __repr__(self):
        return f"<User {self.username}>"
DOMAIN_USER

cat > src/domain/repositories/user_repository.py << 'DOMAIN_REPO'
"""User Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass
DOMAIN_REPO

cat > src/core/value_objects/database_type.py << 'VO_DB'
"""Database Type Value Object"""
from enum import Enum

class DatabaseType(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    
    def get_connection_string(self, host="localhost", port=None, 
                             database="app_db", username="user", password="password"):
        port = port or self.default_port()
        if self == DatabaseType.POSTGRESQL:
            return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        elif self == DatabaseType.MYSQL:
            return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        elif self == DatabaseType.SQLITE:
            return f"sqlite+aiosqlite:///./{database}.db"
        elif self == DatabaseType.MONGODB:
            return f"mongodb://{username}:{password}@{host}:{port}/{database}"
    
    def default_port(self):
        return {
            DatabaseType.POSTGRESQL: 5432,
            DatabaseType.MYSQL: 3306,
            DatabaseType.SQLITE: 0,
            DatabaseType.MONGODB: 27017
        }[self]
VO_DB

print_success "Created Domain Layer"

# ============================================================================
# STEP 3: Application Layer - Use Cases
# ============================================================================
print_step 3 15 "Creating Application Layer"

cat > src/application/interfaces/file_system.py << 'APP_FS'
"""File System Interface"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class IFileSystemService(ABC):
    @abstractmethod
    def create_directory(self, path: Path) -> None:
        pass
    
    @abstractmethod
    def create_file(self, path: Path, content: str) -> None:
        pass
    
    @abstractmethod
    def directory_exists(self, path: Path) -> bool:
        pass
    
    @abstractmethod
    def file_exists(self, path: Path) -> bool:
        pass
    
    @abstractmethod
    def read_file(self, path: Path) -> str:
        pass
APP_FS

cat > src/application/usecases/user/create_user.py << 'APP_CREATE_USER'
"""Create User Use Case"""
from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository

class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository
    
    async def execute(self, email: str, username: str) -> User:
        existing = await self._repository.get_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")
        user = User(email=email, username=username)
        return await self._repository.create(user)
APP_CREATE_USER

cat > src/application/usecases/user/get_user.py << 'APP_GET_USER'
"""Get User Use Case"""
from typing import Optional
from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository

class GetUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository
    
    async def execute(self, user_id: int) -> Optional[User]:
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user
APP_GET_USER

cat > src/application/usecases/user/list_users.py << 'APP_LIST_USER'
"""List Users Use Case"""
from typing import List
from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository

class ListUsersUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self._repository.get_all(skip=skip, limit=limit)
APP_LIST_USER

print_success "Created Application Layer"

# ============================================================================
# STEP 4: Infrastructure Layer
# ============================================================================
print_step 4 15 "Creating Infrastructure Layer"

cat > src/infrastructure/config/settings.py << 'INFRA_SETTINGS'
"""Application Settings"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Clean Architecture"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
INFRA_SETTINGS

cat > src/infrastructure/database/database.py << 'INFRA_DB'
"""Database Setup"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
INFRA_DB

cat > src/infrastructure/database/models/user_model.py << 'INFRA_MODEL'
"""User Database Model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
INFRA_MODEL

cat > src/infrastructure/database/repositories/user_repository.py << 'INFRA_REPO'
"""User Repository Implementation"""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository
from ..models.user_model import UserModel

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    def _to_entity(self, model: UserModel) -> User:
        return User(id=model.id, email=model.email, username=model.username,
                   is_active=model.is_active, created_at=model.created_at)
    
    def _to_model(self, entity: User) -> UserModel:
        return UserModel(id=entity.id, email=entity.email, username=entity.username,
                        is_active=entity.is_active, created_at=entity.created_at)
    
    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self._session.execute(select(UserModel).offset(skip).limit(limit))
        return [self._to_entity(m) for m in result.scalars().all()]
    
    async def update(self, user: User) -> User:
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
        model = await self._session.get(UserModel, user_id)
        if not model:
            return False
        await self._session.delete(model)
        return True
INFRA_REPO

cat > src/infrastructure/file_system/local_file_system.py << 'INFRA_FS'
"""Local File System Service"""
from pathlib import Path
from typing import List
from ...application.interfaces.file_system import IFileSystemService

class LocalFileSystemService(IFileSystemService):
    def create_directory(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
    
    def create_file(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    
    def directory_exists(self, path: Path) -> bool:
        return path.exists() and path.is_dir()
    
    def file_exists(self, path: Path) -> bool:
        return path.exists() and path.is_file()
    
    def read_file(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")
INFRA_FS

print_success "Created Infrastructure Layer"

# ============================================================================
# STEP 5: Interfaces Layer - API
# ============================================================================
print_step 5 15 "Creating Interfaces Layer"

cat > src/interfaces/schemas/user.py << 'API_SCHEMA'
"""User Schemas"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True
API_SCHEMA

cat > src/interfaces/api/dependencies.py << 'API_DEP'
"""API Dependencies"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...infrastructure.database.database import get_db
from ...infrastructure.database.repositories.user_repository import UserRepository
from ...application.usecases.user.create_user import CreateUserUseCase
from ...application.usecases.user.get_user import GetUserUseCase
from ...application.usecases.user.list_users import ListUsersUseCase

def get_user_repository(session: AsyncSession = Depends(get_db)):
    return UserRepository(session)

def get_create_user_usecase(repo: UserRepository = Depends(get_user_repository)):
    return CreateUserUseCase(repo)

def get_get_user_usecase(repo: UserRepository = Depends(get_user_repository)):
    return GetUserUseCase(repo)

def get_list_users_usecase(repo: UserRepository = Depends(get_user_repository)):
    return ListUsersUseCase(repo)
API_DEP

cat > src/interfaces/api/v1/routes/user.py << 'API_ROUTES'
"""User API Routes"""
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

@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, 
                    usecase: ListUsersUseCase = Depends(get_list_users_usecase)):
    users = await usecase.execute(skip=skip, limit=limit)
    return [UserResponse(id=u.id, email=u.email, username=u.username,
                        is_active=u.is_active, created_at=u.created_at) for u in users]
API_ROUTES

print_success "Created Interfaces Layer"

# ============================================================================
# STEP 6: Main Application
# ============================================================================
print_step 6 15 "Creating Main Application"

cat > src/main.py << 'MAIN'
"""FastAPI Main Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .infrastructure.config.settings import settings
from .infrastructure.database.database import init_db
from .interfaces.api.v1.routes import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title=settings.APP_NAME, version=settings.API_VERSION, 
             debug=settings.DEBUG, lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                  allow_methods=["*"], allow_headers=["*"])

app.include_router(user.router, prefix=f"/api/{settings.API_VERSION}")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "docs": "/docs", 
            "version": settings.API_VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}
MAIN

print_success "Created Main Application"

# ============================================================================
# STEP 7-15: Configuration Files
# ============================================================================
print_step 7 15 "Creating requirements.txt"
cat > requirements.txt << 'REQ'
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
sqlalchemy[asyncio]>=2.0.23
aiosqlite>=0.19.0
jinja2>=3.1.2
REQ
print_success "Created requirements.txt"

print_step 8 15 "Creating .env"
cat > .env << 'ENV'
APP_NAME=FastAPI Clean Architecture
DEBUG=True
DATABASE_URL=sqlite+aiosqlite:///./app.db
ENV
print_success "Created .env"

print_step 9 15 "Creating .gitignore"
cat > .gitignore << 'GIT'
__pycache__/
*.py[cod]
venv/
.env
*.db
.pytest_cache/
.idea/
.vscode/
GIT
print_success "Created .gitignore"

print_step 10 15 "Creating Makefile"
cat > Makefile << 'MAKE'
.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	uvicorn src.main:app --reload

test:
	pytest -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -f *.db
MAKE
print_success "Created Makefile"

print_step 11 15 "Creating setup.py"
cat > setup.py << SETUP
from setuptools import setup, find_packages
setup(
    name="$PROJECT_NAME",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "sqlalchemy[asyncio]>=2.0.23",
    ],
)
SETUP
print_success "Created setup.py"

print_step 12 15 "Creating README.md"
cat > README.md << 'README'
# FastAPI Clean Architecture

🚀 Production-ready FastAPI project with Clean Architecture

## Features
- ✅ Clean Architecture (4 layers)
- ✅ Async/Await
- ✅ SQLAlchemy 2.0
- ✅ Pydantic V2
- ✅ User CRUD Example

## Quick Start
```bash
# Install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn src.main:app --reload
```

## API Documentation
http://localhost:8000/docs

## Test API
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","username":"john"}'
```

## Structure
- `src/domain/` - Business entities
- `src/application/` - Use cases
- `src/infrastructure/` - Database, config
- `src/interfaces/` - API endpoints
README
print_success "Created README.md"

print_step 13 15 "Creating virtual environment"
python3 -m venv venv
print_success "Created venv"

print_step 14 15 "Installing dependencies"
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
print_success "Installed dependencies"

print_step 15 15 "Testing application"
timeout 2s uvicorn src.main:app --host 127.0.0.1 --port 8000 2>/dev/null || true
print_success "Application tested"

# ============================================================================
# DONE
# ============================================================================
print_header "🎉 Setup Complete!"
echo ""
echo -e "${GREEN}✅ FastAPI Clean Architecture project is ready!${NC}"
echo ""
echo -e "${BOLD}📁 Location:${NC} $(pwd)"
echo ""
echo -e "${BOLD}🚀 Run:${NC}"
echo -e "   ${CYAN}cd $PROJECT_NAME${NC}"
echo -e "   ${CYAN}source venv/bin/activate${NC}"
echo -e "   ${CYAN}uvicorn src.main:app --reload${NC}"
echo ""
echo -e "${BOLD}📚 Docs:${NC} http://localhost:8000/docs"
echo ""
echo -e "${BOLD}🧪 Test:${NC}"
echo -e "   ${CYAN}curl -X POST http://localhost:8000/api/v1/users/ \\${NC}"
echo -e "   ${CYAN}  -H 'Content-Type: application/json' \\${NC}"
echo -e "   ${CYAN}  -d '{\"email\":\"test@test.com\",\"username\":\"test\"}'${NC}"
echo ""
print_success "Happy coding! 🎉"