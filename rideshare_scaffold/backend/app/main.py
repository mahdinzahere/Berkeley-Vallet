from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import engine
from .models import Base
from .socket_manager import sio
from .routes import auth, rides, drivers, tips, webhooks, ai

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Rideshare API",
    description="UC Berkeley Rideshare Pilot API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(rides.router)
app.include_router(drivers.router)
app.include_router(tips.router)
app.include_router(webhooks.router)
app.include_router(ai.router)

# Create Socket.IO app
socket_app = sio.ASGIApp(sio, app)

# Mount Socket.IO app
app.mount("/ws", socket_app)

# Serve web dashboard
@app.get("/dashboard")
async def get_dashboard():
    """Serve the web dashboard"""
    web_path = Path(__file__).parent / "web" / "index.html"
    if web_path.exists():
        return FileResponse(web_path)
    return {"message": "Dashboard not found"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Rideshare API is running",
        "endpoints": {
            "dashboard": "/dashboard",
            "api_docs": "/docs",
            "socket_io": "/ws",
            "health": "/health"
        }
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Socket.IO health check
@app.get("/socket-health")
async def socket_health():
    return {"status": "healthy", "socket_io": "enabled"}
