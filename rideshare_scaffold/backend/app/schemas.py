from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import UserRole, RideStatus

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    phone: str
    role: UserRole

class UserCreate(UserBase):
    password: str
    name: str

class UserResponse(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Google OAuth schemas
class GoogleUser(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Auth schemas
class MagicLinkRequest(BaseModel):
    email: EmailStr
    phone: str
    role: UserRole

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    phone: str
    code: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Driver Profile schemas
class DriverProfileBase(BaseModel):
    vehicle_make: str
    vehicle_model: str
    vehicle_year: int
    license_plate: str

class DriverProfileCreate(DriverProfileBase):
    pass

class DriverProfileResponse(DriverProfileBase):
    id: int
    user_id: int
    stripe_account_id: Optional[str]
    is_online: bool
    current_latitude: Optional[float]
    current_longitude: Optional[float]
    total_rides: int
    total_earnings: float
    rating: float
    
    class Config:
        from_attributes = True

class DriverLocationUpdate(BaseModel):
    latitude: float
    longitude: float

class DriverOnlineStatus(BaseModel):
    is_online: bool

# Ride schemas
class RideRequest(BaseModel):
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_address: str
    dropoff_latitude: float
    dropoff_longitude: float

class RideQuoteResponse(BaseModel):
    fare: float
    distance_miles: float
    estimated_time_minutes: int

class RideResponse(BaseModel):
    id: int
    rider_id: int
    driver_id: Optional[int]
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_address: str
    dropoff_latitude: float
    dropoff_longitude: float
    status: RideStatus
    fare: float
    distance_miles: float
    payment_intent_id: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class RideStatusUpdate(BaseModel):
    status: RideStatus

# Tip schemas
class TipRequest(BaseModel):
    ride_id: int
    amount: float

class TipResponse(BaseModel):
    id: int
    ride_id: int
    from_user_id: int
    to_user_id: int
    amount: float
    payment_intent_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Stripe schemas
class StripeConnectResponse(BaseModel):
    account_link: str
    account_id: str
