import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # --- 1. BASE PATHS ---
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # Storage Directories
    UPLOAD_DIR = DATA_DIR / "uploads"
    # This reads "vector_db" from your .env or uses default
    CHROMA_DB_DIR = DATA_DIR / os.getenv("CHROMA_DB_PATH", "vector_db") 

    # --- 2. APP SETTINGS ---
    PROJECT_NAME = os.getenv("PROJECT_NAME", "AI Personal Tax Assistant")
    APP_VERSION = os.getenv("VERSION", "0.1.0")
    
    # --- 3. DATABASE SETTINGS (This was missing!) ---
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "tax_documents")

    # --- 4. PROCESSING CONSTANTS ---
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 20))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
    TOP_K = int(os.getenv("TOP_K", 3))

    # --- 5. AI MODELS (OLLAMA) ---
    LLM_MODEL = os.getenv("LLM_MODEL", "mistral:7b")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # --- 6. NETWORK & CORS ---
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))
    API_PREFIX = os.getenv("API_PREFIX", "/api")
    
    # Construct Full Backend URL
    BACKEND_URL = f"http://{HOST}:{PORT}{API_PREFIX}"
    
    # Frontend URL (For CORS whitelist)
    FRONTEND_HOST = os.getenv("FRONTEND_HOST", "localhost")
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8501))
    FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

# Create the global settings object
settings = Settings()

# --- AUTOMATIC DIRECTORY CREATION ---
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)