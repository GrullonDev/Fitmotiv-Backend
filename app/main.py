from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import (
    auth_router, exercise_router, routine_router, nutrition_router,
    progress_router, notification_router, motivation_router, user_router,
    profile_router, goals_router, weight_progress_router, workouts_router
)
from app.config import get_settings

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Backend API para FitMotiv - Aplicación de fitness y motivación con perfiles extendidos",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directories
upload_dirs = ["uploads/profiles", "uploads/progress", "uploads/covers"]
for directory in upload_dirs:
    os.makedirs(directory, exist_ok=True)

# Mount static files for file uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include all routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(profile_router.router)
app.include_router(goals_router.router)
app.include_router(weight_progress_router.router)
app.include_router(workouts_router.router)
app.include_router(exercise_router.router)
app.include_router(routine_router.router)
app.include_router(nutrition_router.router)
app.include_router(progress_router.router)
app.include_router(notification_router.router)
app.include_router(motivation_router.router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a FitMotiv API v3.0",
        "version": "3.0.0",
        "status": "running",
        "features": [
            "Perfiles de usuario extendidos",
            "Sistema de objetivos fitness avanzado",
            "Seguimiento de peso corporal",
            "Rutinas diarias de ejercicio",
            "Frases motivacionales",
            "Sistema de notificaciones",
            "Análisis de progreso"
        ],
        "endpoints": {
            "auth": "/api/auth",
            "users": "/api/users",
            "profiles": "/api/profiles", 
            "goals": "/api/goals",
            "weight": "/api/weight",
            "workouts": "/api/workouts",
            "exercises": "/api/exercises",
            "routines": "/api/routines",
            "nutrition": "/api/nutrition",
            "progress": "/api/progress",
            "notifications": "/api/notifications",
            "motivation": "/api/motivation"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
