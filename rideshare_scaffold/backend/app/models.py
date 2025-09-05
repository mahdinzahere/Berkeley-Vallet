from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from .database import Base

class UserRole(PyEnum):
    RIDER = "rider"
    DRIVER = "driver"

class RideStatus(PyEnum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    ARRIVED = "arrived"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)  # Nullable for Google OAuth users
    role = Column(Enum(UserRole), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    driver_profile = relationship("DriverProfile", back_populates="user", uselist=False)
    rides_as_rider = relationship("Ride", foreign_keys="Ride.rider_id", back_populates="rider")
    rides_as_driver = relationship("Ride", foreign_keys="Ride.driver_id", back_populates="driver")
    tips_given = relationship("Tip", foreign_keys="Tip.from_user_id", back_populates="from_user")
    tips_received = relationship("Tip", foreign_keys="Tip.to_user_id", back_populates="to_user")

class DriverProfile(Base):
    __tablename__ = "driver_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    vehicle_make = Column(String)
    vehicle_model = Column(String)
    vehicle_year = Column(Integer)
    license_plate = Column(String)
    stripe_account_id = Column(String)
    is_online = Column(Boolean, default=False)
    current_latitude = Column(Float)
    current_longitude = Column(Float)
    total_rides = Column(Integer, default=0)
    total_earnings = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="driver_profile")

class Ride(Base):
    __tablename__ = "rides"
    
    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    pickup_address = Column(String)
    pickup_latitude = Column(Float)
    pickup_longitude = Column(Float)
    dropoff_address = Column(String)
    dropoff_latitude = Column(Float)
    dropoff_longitude = Column(Float)
    status = Column(Enum(RideStatus), default=RideStatus.REQUESTED)
    fare = Column(Float)
    distance_miles = Column(Float)
    payment_intent_id = Column(String)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    rider = relationship("User", foreign_keys=[rider_id], back_populates="rides_as_rider")
    driver = relationship("User", foreign_keys=[driver_id], back_populates="rides_as_driver")
    tips = relationship("Tip", back_populates="ride")

class Tip(Base):
    __tablename__ = "tips"
    
    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"))
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    payment_intent_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ride = relationship("Ride", back_populates="tips")
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="tips_given")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="tips_received")
