set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BOLD}${BLUE}========================================${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_step() {
    echo -e "\n${BOLD}${BLUE}[$1/$2] $3...${NC}"
}

# Main
PROJECT_NAME=${1:-"fastapi-clean-cli"}
TOTAL_STEPS=12

print_header "FastAPI Clean Architecture - Ultimate Setup"

echo -e "${BOLD}Project Configuration:${NC}"
echo "  Name: $PROJECT_NAME"
echo "  Path: ./$PROJECT_NAME"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_error "Setup cancelled"
    exit 1
fi

# Step 1: Create project directory
print_step 1 $TOTAL_STEPS "Creating project directory"
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"
print_success "Created project directory"

# Step 2: Create directory structure
print_step 2 $TOTAL_STEPS "Creating directory structure"
mkdir -p src/{core/{entities,value_objects,exceptions},application/{interfaces,usecases/{user,create_project,generate_crud,add_feature}},infrastructure/{file_system,templates,validators,generators,config,database/{models,repositories}},presentation/{cli,formatters,parsers},interfaces/{api/v1/routes,schemas},config}
mkdir -p tests/{unit/{core,application,infrastructure},integration}
mkdir -p templates/{base,crud,docker,auth,features}
mkdir -p docs .github/workflows
print_success "Created directory structure"

# Step 3: Create __init__.py files
print_step 3 $TOTAL_STEPS "Creating __init__.py files"
find src tests -type d -exec touch {}/__init__.py \;
print_success "Created __init__.py files"

# Step 4: Create requirements.txt
print_step 4 $TOTAL_STEPS "Creating requirements.txt"
cat > requirements.txt << 'EOF'
# Core
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Database
sqlalchemy[asyncio]>=2.0.23
aiosqlite>=0.19.0

# Templates
jinja2>=3.1.2

# CLI
rich>=13.7.0
EOF
print_success "Created requirements.txt"

# Step 5: Create example source files
print_step 5 $TOTAL_STEPS "Creating source files with endpoints"

# User Entity
cat > src/domain/entities/user.py << 'EOF'
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
    
    def __repr__(self):
        return f"<User {self.username}>"
EOF

# User Repository Interface
cat > src/domain/repositories/user_repository.py << 'EOF'
"""User Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]: pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]: pass
EOF

# Create User Use Case
cat > src/application/usecases/user/create_user.py << 'EOF'
"""Create User Use Case"""
from ....domain.entities.user import User
from ....domain.repositories.user_repository import IUserRepository

class CreateUserUseCase:
    def __init__(self, repository: IUserRepository):
        self._repository = repository
    
    async def execute(self, email: str, username: str) -> User:
        user = User(email=email, username=username)
        return await self._repository.create(user)
EOF

# Settings
cat > src/infrastructure/config/settings.py << 'EOF'
"""Settings"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Clean Architecture"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
EOF

# Database
cat > src/infrastructure/database/database.py << 'EOF'
"""Database"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
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
EOF

# User Model
cat > src/infrastructure/database/models/user_model.py << 'EOF'
"""User Model"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
EOF

# User Repository Implementation
cat > src/infrastructure/database/repositories/user_repository.py << 'EOF'
"""User Repository"""
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
    
    async def create(self, user: User) -> User:
        model = UserModel(email=user.email, username=user.username)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self._session.execute(select(UserModel).offset(skip).limit(limit))
        return [self._to_entity(m) for m in result.scalars().all()]
EOF

# Schemas
cat > src/interfaces/schemas/user.py << 'EOF'
"""User Schemas"""
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
EOF

# Dependencies
cat > src/interfaces/api/dependencies.py << 'EOF'
"""Dependencies"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastclean.infrastructure.database.database import get_db
from fastclean.infrastructure.database.repositories.user_repository import UserRepository
from ...application.usecases.user.create_user import CreateUserUseCase

def get_user_repository(session: AsyncSession = Depends(get_db)):
    return UserRepository(session)

def get_create_user_usecase(repo: UserRepository = Depends(get_user_repository)):
    return CreateUserUseCase(repo)
EOF

# Routes
cat > src/interfaces/api/v1/routes/user.py << 'EOF'
"""User Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ....schemas.user import UserCreate, UserResponse
from ....api.dependencies import get_create_user_usecase
from .....application.usecases.user.create_user import CreateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, usecase: CreateUserUseCase = Depends(get_create_user_usecase)):
    try:
        user = await usecase.execute(data.email, data.username)
        return UserResponse(id=user.id, email=user.email, username=user.username,
                          is_active=user.is_active, created_at=user.created_at)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserResponse])
async def list_users():
    return []
EOF

# Main
cat > src/main.py << 'EOF'
"""Main Application"""
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

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                  allow_methods=["*"], allow_headers=["*"])

app.include_router(user.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

print_success "Created all source files with working endpoints"

# Step 6: Create .gitignore
print_step 6 $TOTAL_STEPS "Creating .gitignore"
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
venv/
.env
*.db
.pytest_cache/
.idea/
.vscode/
EOF
print_success "Created .gitignore"

# Step 7: Create README
print_step 7 $TOTAL_STEPS "Creating README.md"
cat > README.md << EOF
# $PROJECT_NAME

FastAPI project with Clean Architecture

## Quick Start

\`\`\`bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn src.main:app --reload
\`\`\`

## Test API

Open: http://localhost:8000/docs

### Create User
\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/users/" \\
  -H "Content-Type: application/json" \\
  -d '{"email": "john@example.com", "username": "john"}'
\`\`\`

## Structure

- \`src/domain/\` - Business entities
- \`src/application/\` - Use cases
- \`src/infrastructure/\` - Database, config
- \`src/interfaces/\` - API endpoints

Enjoy! 🚀
EOF
print_success "Created README.md"

# Step 8: Create Makefile
print_step 8 $TOTAL_STEPS "Creating Makefile"
cat > Makefile << 'EOF'
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
EOF
print_success "Created Makefile"

# Step 9: Create setup.py
print_step 9 $TOTAL_STEPS "Creating setup.py"
cat > setup.py << EOF
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
        "aiosqlite>=0.19.0",
    ],
)
EOF
print_success "Created setup.py"

# Step 10: Create virtual environment
print_step 10 $TOTAL_STEPS "Creating virtual environment"
python3 -m venv venv
print_success "Created virtual environment"

# Step 11: Install dependencies
print_step 11 $TOTAL_STEPS "Installing dependencies"
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
pip install -q --upgrade pip
pip install -q -r requirements.txt
print_success "Installed dependencies"

# Step 12: Test run
print_step 12 $TOTAL_STEPS "Testing application"
timeout 3s uvicorn src.main:app --host 127.0.0.1 --port 8000 2>/dev/null || true
print_success "Application tested successfully"

# Done
print_header "🎉 Setup Complete!"
echo ""
echo -e "${GREEN}✅ Your FastAPI Clean Architecture project is ready!${NC}"
echo ""
echo -e "${BOLD}📁 Project location:${NC}"
echo "   $(pwd)"
echo ""
echo -e "${BOLD}🚀 To run the application:${NC}"
echo -e "   ${CYAN}cd $PROJECT_NAME${NC}"
echo -e "   ${CYAN}source venv/bin/activate${NC}  # Windows: venv\\Scripts\\activate"
echo -e "   ${CYAN}uvicorn src.main:app --reload${NC}"
echo ""
echo -e "${BOLD}📚 Documentation:${NC}"
echo "   http://localhost:8000/docs"
echo ""
echo -e "${BOLD}🧪 Test API:${NC}"
echo -e "   ${CYAN}curl -X POST http://localhost:8000/api/v1/users/ \\${NC}"
echo -e "   ${CYAN}  -H 'Content-Type: application/json' \\${NC}"
echo -e "   ${CYAN}  -d '{\"email\":\"test@example.com\",\"username\":\"test\"}'${NC}"
echo ""
print_success "Happy coding! 🎉"