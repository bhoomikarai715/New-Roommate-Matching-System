import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.database import engine, Base, SessionLocal, init_db
from backend.routes import auth, profile, matches, chat, agreement
from backend.services.seeder import seed_database
from backend.config import settings

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Handle read-only filesystems in serverless environments (like Vercel)
    try:
        # Proper initialization sequence
        init_db()
    except Exception as e:
        print(f"Skipping database init in serverless environment: {e}")
        
    yield
    # Shutdown logic if any

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Serve static files from the root directory
# We determine the root directory relative to this file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Include Routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(matches.router)
app.include_router(chat.router)
app.include_router(agreement.router)

# Mount static files (excluding /api which is handled by routers)
app.mount("/static", StaticFiles(directory=base_dir), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(base_dir, "index.html"))

@app.get("/{filename}")
def serve_root_files(filename: str):
    file_path = os.path.join(base_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
