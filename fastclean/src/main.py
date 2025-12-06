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