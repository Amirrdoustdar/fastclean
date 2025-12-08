#!/usr/bin/env python3
"""
Template Builder Script
Automatically creates all Jinja2 template files
Usage: python build_templates.py
"""

from pathlib import Path
from typing import Dict

# Template content definitions
TEMPLATES = {
    # ==================== BASE TEMPLATES ====================
    "base/main.py.j2": '''"""{{ project_name }} - FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .infrastructure.config.settings import settings
from .interfaces.api.v1.routes import user

app = FastAPI(
    title="{{ project_name }}",
    description="API built with Clean Architecture",
    version="1.0.0",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/{{ api_version }}")

@app.get("/")
async def root():
    return {
        "message": "Welcome to {{ project_name }}",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
''',

    "base/settings.py.j2": '''"""Application Settings"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "{{ project_name }}"
    DEBUG: bool = True
    API_VERSION: str = "{{ api_version }}"
    DATABASE_URL: str = "{{ database_url }}"
    {% if auth_type == 'jwt' %}
    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    {% endif %}
    
    class Config:
        env_file = ".env"

settings = Settings()
''',

    "base/database.py.j2": '''"""Database connection"""
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
''',

    "base/env.j2": '''# {{ project_name }} Environment Variables
APP_NAME={{ project_name }}
DEBUG=True
DATABASE_URL={{ database_url }}
{% if auth_type == 'jwt' %}
SECRET_KEY=your-secret-key-change-in-production
{% endif %}
''',

    "base/gitignore.j2": '''__pycache__/
*.py[cod]
venv/
.env
*.db
.pytest_cache/
.coverage
.idea/
.vscode/
''',

    "base/readme.md.j2": '''# {{ project_name }}

FastAPI project with Clean Architecture

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Documentation
- Swagger: http://localhost:8000/docs
''',

    # ==================== CRUD TEMPLATES ====================
    "crud/entity.py.j2": '''"""{{ entity_name }} Entity"""
from datetime import datetime
from typing import Optional

class {{ entity_name }}:
    def __init__(
        self,
        {% for field in fields %}{{ field.name }}: {{ field.type }},
        {% endfor %}id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        {% for field in fields %}self.{{ field.name }} = {{ field.name }}
        {% endfor %}self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"<{{ entity_name }} {self.id}>"
''',

    "crud/repository_interface.py.j2": '''"""{{ entity_name }} Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.{{ entity_name_snake }} import {{ entity_name }}

class I{{ entity_name }}Repository(ABC):
    @abstractmethod
    async def create(self, entity: {{ entity_name }}) -> {{ entity_name }}:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[{{ entity_name }}]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[{{ entity_name }}]:
        pass
    
    @abstractmethod
    async def update(self, entity: {{ entity_name }}) -> {{ entity_name }}:
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
''',

    "crud/model.py.j2": '''"""{{ entity_name }} Database Model"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from ..database import Base

class {{ entity_name }}Model(Base):
    __tablename__ = "{{ entity_name_snake }}s"
    
    id = Column(Integer, primary_key=True, index=True)
    {% for field in fields %}{% if field.type == 'str' %}{{ field.name }} = Column(String)
    {% elif field.type == 'int' %}{{ field.name }} = Column(Integer)
    {% elif field.type == 'float' %}{{ field.name }} = Column(Float)
    {% elif field.type == 'bool' %}{{ field.name }} = Column(Boolean, default=True)
    {% endif %}{% endfor %}created_at = Column(DateTime, default=datetime.now)
''',

    "crud/repository_impl.py.j2": '''"""{{ entity_name }} Repository Implementation"""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.entities.{{ entity_name_snake }} import {{ entity_name }}
from ....domain.repositories.{{ entity_name_snake }}_repository import I{{ entity_name }}Repository
from ..models.{{ entity_name_snake }}_model import {{ entity_name }}Model

class {{ entity_name }}Repository(I{{ entity_name }}Repository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    def _to_entity(self, model: {{ entity_name }}Model) -> {{ entity_name }}:
        return {{ entity_name }}(
            id=model.id,
            {% for field in fields %}{{ field.name }}=model.{{ field.name }},
            {% endfor %}created_at=model.created_at
        )
    
    async def create(self, entity: {{ entity_name }}) -> {{ entity_name }}:
        model = {{ entity_name }}Model(
            {% for field in fields %}{{ field.name }}=entity.{{ field.name }},
            {% endfor %})
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)
    
    async def get_by_id(self, id: int) -> Optional[{{ entity_name }}]:
        result = await self._session.execute(
            select({{ entity_name }}Model).where({{ entity_name }}Model.id == id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[{{ entity_name }}]:
        result = await self._session.execute(
            select({{ entity_name }}Model).offset(skip).limit(limit)
        )
        return [self._to_entity(m) for m in result.scalars().all()]
    
    async def update(self, entity: {{ entity_name }}) -> {{ entity_name }}:
        model = await self._session.get({{ entity_name }}Model, entity.id)
        if model:
            {% for field in fields %}model.{{ field.name }} = entity.{{ field.name }}
            {% endfor %}await self._session.flush()
            await self._session.refresh(model)
            return self._to_entity(model)
        raise ValueError("Not found")
    
    async def delete(self, id: int) -> bool:
        model = await self._session.get({{ entity_name }}Model, id)
        if model:
            await self._session.delete(model)
            return True
        return False
''',

    "crud/usecase_create.py.j2": '''"""Create {{ entity_name }} Use Case"""
from ....domain.entities.{{ entity_name_snake }} import {{ entity_name }}
from ....domain.repositories.{{ entity_name_snake }}_repository import I{{ entity_name }}Repository

class Create{{ entity_name }}UseCase:
    def __init__(self, repository: I{{ entity_name }}Repository):
        self._repository = repository
    
    async def execute(self, {% for field in fields %}{{ field.name }}: {{ field.type }}, {% endfor %}) -> {{ entity_name }}:
        entity = {{ entity_name }}({% for field in fields %}{{ field.name }}={{ field.name }}, {% endfor %})
        return await self._repository.create(entity)
''',

    "crud/routes.py.j2": '''"""{{ entity_name }} API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ....schemas.{{ entity_name_snake }} import {{ entity_name }}Create, {{ entity_name }}Response

router = APIRouter(prefix="/{{ entity_name_snake }}s", tags=["{{ entity_name_snake }}s"])

@router.post("/", response_model={{ entity_name }}Response, status_code=201)
async def create(data: {{ entity_name }}Create):
    # TODO: Implement with use case
    pass

@router.get("/{id}", response_model={{ entity_name }}Response)
async def get(id: int):
    # TODO: Implement with use case
    pass

@router.get("/", response_model=list[{{ entity_name }}Response])
async def list_all(skip: int = 0, limit: int = 100):
    # TODO: Implement with use case
    pass
''',

    "crud/schemas.py.j2": '''"""{{ entity_name }} Schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class {{ entity_name }}Base(BaseModel):
    {% for field in fields %}{{ field.name }}: {{ field.type }}
    {% endfor %}

class {{ entity_name }}Create({{ entity_name }}Base):
    pass

class {{ entity_name }}Update(BaseModel):
    {% for field in fields %}{{ field.name }}: Optional[{{ field.type }}] = None
    {% endfor %}

class {{ entity_name }}Response({{ entity_name }}Base):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
''',

    # ==================== DOCKER TEMPLATES ====================
    "docker/dockerfile.j2": '''FROM python:{{ python_version }}-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
''',

    "docker/docker_compose.yml.j2": '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL={{ database_url }}
    {% if database_type == 'postgresql' %}depends_on:
      - postgres
    {% endif %}
    volumes:
      - .:/app

{% if database_type == 'postgresql' %}
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: {{ project_name }}_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
{% endif %}
''',

    # ==================== AUTH TEMPLATES ====================
    "auth/jwt_handler.py.j2": '''"""JWT Handler"""
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from ...config.settings import settings

class JWTHandler:
    def __init__(self):
        self.secret = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.pwd_context.verify(plain, hashed)
''',
}


def create_templates(base_path: Path = Path("templates")):
    """Create all template files"""
    print(f"🚀 Creating templates in: {base_path}")
    
    # Create base directory
    base_path.mkdir(exist_ok=True)
    
    created_count = 0
    
    for template_path, content in TEMPLATES.items():
        # Full path
        full_path = base_path / template_path
        
        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        full_path.write_text(content, encoding="utf-8")
        print(f"  ✅ Created: {template_path}")
        created_count += 1
    
    print(f"\n✨ Successfully created {created_count} template files!")
    print(f"📁 Location: {base_path.absolute()}")
    print("\n📝 Directory structure:")
    print_tree(base_path)


def print_tree(directory: Path, prefix: str = "", is_last: bool = True):
    """Print directory tree"""
    if directory.name.startswith('.'):
        return
    
    connector = "└── " if is_last else "├── "
    print(f"{prefix}{connector}{directory.name}")
    
    if directory.is_dir():
        children = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            extension = "    " if is_last else "│   "
            print_tree(child, prefix + extension, is_last_child)


def main():
    """Main function"""
    print("=" * 60)
    print("  FastAPI Clean Architecture - Template Builder")
    print("=" * 60)
    print()
    
    # Ask for path
    default_path = Path("templates")
    user_input = input(f"Enter templates directory path (default: {default_path}): ").strip()
    
    templates_path = Path(user_input) if user_input else default_path
    
    # Confirm
    print(f"\n📍 Will create templates in: {templates_path.absolute()}")
    confirm = input("Continue? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    print()
    create_templates(templates_path)
    
    print("\n" + "=" * 60)
    print("✨ Done! You can now use these templates with the CLI tool.")
    print("=" * 60)


if __name__ == "__main__":
    main()