from pathlib import Path
from typing import List
from ..base import BaseUseCase
from .dto import AddAuthenticationRequest, AddFeatureResponse
from fastclean.application.interfaces.file_system import IFileSystemService
from fastclean.application.interfaces.template_engine import ITemplateEngine
from fastclean.core.exceptions.validation import InvalidPathException


class AddAuthenticationUseCase(BaseUseCase[AddAuthenticationRequest, AddFeatureResponse]):
    """Use case for adding authentication to existing project"""
    
    def __init__(
        self,
        file_system: IFileSystemService,
        template_engine: ITemplateEngine
    ):
        self._file_system = file_system
        self._template_engine = template_engine
    
    def execute(self, request: AddAuthenticationRequest) -> AddFeatureResponse:
        """Execute authentication addition"""
        # Validate
        self.validate_input(request)
        
        files_created = []
        files_modified = []
        
        # Generate authentication files based on type
        if request.auth_type == 'jwt':
            files_created.extend(self._add_jwt_auth(request))
        elif request.auth_type == 'oauth2':
            files_created.extend(self._add_oauth2_auth(request))
        elif request.auth_type == 'api_key':
            files_created.extend(self._add_api_key_auth(request))
        else:
            raise ValueError(f"Unsupported auth type: {request.auth_type}")
        
        # Update main.py to include auth routes
        main_path = request.project_path / "src" / "main.py"
        if self._file_system.file_exists(main_path):
            self._update_main_file(main_path, request.auth_type)
            files_modified.append(main_path)
        
        # Update requirements.txt
        requirements_path = request.project_path / "requirements.txt"
        if self._file_system.file_exists(requirements_path):
            self._update_requirements(requirements_path, request.auth_type)
            files_modified.append(requirements_path)
        
        return AddFeatureResponse(
            feature_name=f"authentication_{request.auth_type}",
            files_created=files_created,
            files_modified=files_modified,
            success=True,
            message=f"Successfully added {request.auth_type.upper()} authentication!"
        )
    
    def validate_input(self, request: AddAuthenticationRequest) -> None:
        """Validate input"""
        if not self._file_system.directory_exists(request.project_path):
            raise InvalidPathException(str(request.project_path))
        
        # Check if src directory exists
        src_path = request.project_path / "src"
        if not self._file_system.directory_exists(src_path):
            raise InvalidPathException("Project does not have src/ directory")
        
        # Validate auth type
        valid_types = ['jwt', 'oauth2', 'api_key', 'basic']
        if request.auth_type not in valid_types:
            raise ValueError(f"Auth type must be one of: {', '.join(valid_types)}")
    
    def _add_jwt_auth(self, request: AddAuthenticationRequest) -> list[Path]:
        """Add JWT authentication"""
        files_created = []
        
        # Create auth directory
        auth_dir = request.project_path / "src" / "infrastructure" / "auth"
        self._file_system.create_directory(auth_dir)
        
        # Context for templates
        context = {
            'auth_type': 'jwt',
            'secret_key': request.secret_key or 'your-secret-key-change-in-production'
        }
        
        # JWT Handler
        template = self._template_engine.load_template("jwt_handler", "auth")
        content = self._template_engine.render(template, context)
        jwt_handler_path = auth_dir / "jwt_handler.py"
        self._file_system.create_file(jwt_handler_path, content)
        files_created.append(jwt_handler_path)
        
        # Password Hasher
        password_hasher_content = '''"""Password Hashing Utilities"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)
'''
        password_hasher_path = auth_dir / "password_hasher.py"
        self._file_system.create_file(password_hasher_path, password_hasher_content)
        files_created.append(password_hasher_path)
        
        # Auth Dependencies
        dependencies_content = '''"""Authentication Dependencies"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from .jwt_handler import JWTHandler
from ...domain.entities.user import User
from ...domain.repositories.user_repository import IUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
jwt_handler = JWTHandler()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: IUserRepository = Depends()
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = jwt_handler.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = await user_repository.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
'''
        dependencies_path = auth_dir / "dependencies.py"
        self._file_system.create_file(dependencies_path, dependencies_content)
        files_created.append(dependencies_path)
        
        # Auth Routes
        auth_routes_content = '''"""Authentication API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from ....schemas.auth import Token, UserLogin
from .jwt_handler import JWTHandler
from ...domain.repositories.user_repository import IUserRepository

router = APIRouter(prefix="/auth", tags=["authentication"])
jwt_handler = JWTHandler()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: IUserRepository = Depends()
):
    """Login endpoint"""
    user = await user_repository.get_by_email(form_data.username)
    if not user or not jwt_handler.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = jwt_handler.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
'''
        routes_path = request.project_path / "src" / "interfaces" / "api" / "v1" / "routes" / "auth.py"
        self._file_system.create_file(routes_path, auth_routes_content)
        files_created.append(routes_path)
        
        # Auth Schemas
        auth_schemas_content = '''"""Authentication Schemas"""
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    """Token response"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token data"""
    user_id: int | None = None

class UserLogin(BaseModel):
    """User login"""
    email: EmailStr
    password: str
'''
        schemas_path = request.project_path / "src" / "interfaces" / "schemas" / "auth.py"
        self._file_system.create_file(schemas_path, auth_schemas_content)
        files_created.append(schemas_path)
        
        # Update settings
        self._update_settings_for_jwt(request.project_path, request.secret_key)
        
        return files_created
    
    def _add_oauth2_auth(self, request: AddAuthenticationRequest) -> list[Path]:
        """Add OAuth2 authentication"""
        # TODO: Implement OAuth2
        return []
    
    def _add_api_key_auth(self, request: AddAuthenticationRequest) -> list[Path]:
        """Add API Key authentication"""
        # TODO: Implement API Key auth
        return []
    
    def _update_main_file(self, main_path: Path, auth_type: str) -> None:
        """Update main.py to include auth routes"""
        content = self._file_system.read_file(main_path)
        
        # Add import
        import_line = "from .interfaces.api.v1.routes import auth\n"
        if import_line not in content:
            # Find the last import and add after it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('from .interfaces.api'):
                    lines.insert(i + 1, import_line.strip())
                    break
            
            # Add router
            router_line = 'app.include_router(auth.router, prefix="/api/v1")'
            for i, line in enumerate(lines):
                if 'app.include_router' in line:
                    lines.insert(i + 1, router_line)
                    break
            
            content = '\n'.join(lines)
            self._file_system.create_file(main_path, content)
    
    def _update_requirements(self, requirements_path: Path, auth_type: str) -> None:
        """Update requirements.txt with auth dependencies"""
        content = self._file_system.read_file(requirements_path)
        
        packages = []
        if auth_type == 'jwt':
            packages = [
                'python-jose[cryptography]==3.3.0',
                'passlib[bcrypt]==1.7.4',
                'python-multipart==0.0.6'
            ]
        
        for package in packages:
            if package.split('==')[0] not in content:
                content += f"\n{package}"
        
        self._file_system.create_file(requirements_path, content)
    
    def _update_settings_for_jwt(self, project_path: Path, secret_key: str) -> None:
        """Update settings.py with JWT configuration"""
        settings_path = project_path / "src" / "infrastructure" / "config" / "settings.py"
        
        if self._file_system.file_exists(settings_path):
            content = self._file_system.read_file(settings_path)
            
            jwt_config = f'''
    # JWT Authentication
    SECRET_KEY: str = "{secret_key or 'your-secret-key-change-in-production'}"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
'''
            
            if 'SECRET_KEY' not in content:
                # Add before class Config
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'class Config:' in line:
                        lines.insert(i, jwt_config)
                        break
                
                content = '\n'.join(lines)
                self._file_system.create_file(settings_path, content)