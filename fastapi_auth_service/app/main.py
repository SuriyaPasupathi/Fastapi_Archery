from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from .database import Base
from .models.user import User
from .api.v1 import auth
from .services.auth_service import auth_service
from .core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Role-based authentication service with Super Admin, Client Admin, and Organizer hierarchy",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])


@app.on_event("startup")
async def startup_event():
    """Initialize Super Admin account on startup"""
    db = next(get_db())
    try:
        super_admin = auth_service.initialize_super_admin(db)
        print(f"Super Admin initialized: {super_admin.username}")
    except Exception as e:
        print(f"Error initializing Super Admin: {e}")
    finally:
        db.close()


@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI Auth Service",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
