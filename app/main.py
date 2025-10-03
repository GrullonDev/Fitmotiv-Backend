from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth
from app.routers import exercise_router, routine_router, nutrition_router
from app.routers import progress_router, notification_router, motivation_router
from app.config import get_settings

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Backend API para FitMotiv - Aplicación de fitness y motivación",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers
app.include_router(auth.router)
app.include_router(exercise_router.router)
app.include_router(routine_router.router)
app.include_router(nutrition_router.router)
app.include_router(progress_router.router)
app.include_router(notification_router.router)
app.include_router(motivation_router.router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a FitMotiv API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
