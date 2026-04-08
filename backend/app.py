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

# Include Routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(matches.router)
app.include_router(chat.router)
app.include_router(agreement.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}
