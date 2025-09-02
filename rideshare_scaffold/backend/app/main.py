from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import engine
from .models import Base
# from .socket_manager import sio
# from .routes import auth, rides, drivers, tips, webhooks

# Create database tables
Base.metadata.create_all(bind=engine)  # Temporarily disabled for testing

# Create FastAPI app
app = FastAPI(
    title="Valleyet - Your Trusted Rideshare Partner",
    description="Valleyet Rideshare API - Safe, Reliable, Valleyet",
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

# Include routers - temporarily disabled
# app.include_router(auth.router)
# app.include_router(rides.router)
# app.include_router(drivers.router)
# app.include_router(tips.router)
# app.include_router(webhooks.router)
# app.include_router(ai.router)  # Temporarily disabled - needs OpenAI API key

# Create Socket.IO app
# socket_app = sio.ASGIApp(sio, app)

# Mount Socket.IO app
# app.mount("/ws", socket_app)

# Serve Valleyet main website
@app.get("/")
async def root():
    """Serve the Valleyet main website"""
    web_path = Path(__file__).parent / "web" / "index.html"
    if web_path.exists():
        return FileResponse(web_path)
    return {"message": "Valleyet website not found"}

# Serve rider dashboard
@app.get("/rider-dashboard")
async def get_rider_dashboard():
    """Serve the rider dashboard"""
    rider_path = Path(__file__).parent / "web" / "rider-dashboard.html"
    if rider_path.exists():
        return FileResponse(rider_path)
    return {"message": "Rider dashboard not found"}

# Serve driver dashboard
@app.get("/driver-dashboard")
async def get_driver_dashboard():
    """Serve the driver dashboard"""
    driver_path = Path(__file__).parent / "web" / "driver-dashboard.html"
    if driver_path.exists():
        return FileResponse(driver_path)
    return {"message": "Driver dashboard not found"}

# Serve web dashboard (legacy - redirects to rider dashboard)
@app.get("/dashboard")
async def get_dashboard():
    """Serve the web dashboard"""
    rider_path = Path(__file__).parent / "web" / "rider-dashboard.html"
    if rider_path.exists():
        return FileResponse(rider_path)
    return {"message": "Dashboard not found"}

# Serve login page
@app.get("/login")
async def get_login():
    """Serve the login page"""
    login_path = Path(__file__).parent / "web" / "login.html"
    if login_path.exists():
        return FileResponse(login_path)
    return {"message": "Login page not found"}

# API info endpoint
@app.get("/api")
async def api_info():
    return {
        "message": "Valleyet API is running",
        "endpoints": {
            "main_website": "/",
            "rider_dashboard": "/rider-dashboard",
            "driver_dashboard": "/driver-dashboard",
            "api_docs": "/docs",
            "login": "/login",
            "health": "/health"
        }
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Valleyet"}

# Socket.IO health check
# @app.get("/socket-health")
# async def socket_health():
#     return {"status": "healthy", "socket_io": "enabled"}

