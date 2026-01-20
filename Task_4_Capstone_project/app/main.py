from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.upload import router as upload_router
from app.api.query import router as query_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION
)


origins = [
    settings.FRONTEND_URL,      
    "http://localhost:8501",    
    "http://127.0.0.1:8501"     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# --- ROUTERS ---
app.include_router(upload_router, prefix=settings.API_PREFIX)
app.include_router(query_router, prefix=settings.API_PREFIX)

@app.get("/")
def health_check():
    return {
        "status": "ok", 
        "message": f"{settings.PROJECT_NAME} is running",
        "version": settings.APP_VERSION
    }