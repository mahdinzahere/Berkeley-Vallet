import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://mahdinzahere@localhost:5432/rideshare")
    
    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Stripe
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    
    # Magic Link
    MAGIC_LINK_EXPIRE_MINUTES: int = 10
    
    # Ride Pricing
    BASE_FARE: float = 2.50
    PER_MILE_RATE: float = 1.75
    
    # Socket.IO
    SOCKET_CORS_ORIGINS: str = "*"

settings = Settings()
