from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, DriverProfile, UserRole
from ..schemas import DriverProfileCreate, DriverProfileResponse, DriverLocationUpdate, DriverOnlineStatus, StripeConnectResponse
from ..auth import get_current_user
from ..stripe_service import StripeService
from ..socket_manager import sio

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.post("/profile", response_model=DriverProfileResponse)
async def create_driver_profile(
    profile: DriverProfileCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Create driver profile"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can create driver profiles"
            )
        
        # Check if profile already exists
        existing_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver profile already exists"
            )
        
        # Create Stripe Connect account
        stripe_account = StripeService.create_connect_account(
            email=current_user.email,
            phone=current_user.phone
        )
        
        # Create driver profile
        driver_profile = DriverProfile(
            user_id=current_user.id,
            vehicle_make=profile.vehicle_make,
            vehicle_model=profile.vehicle_model,
            vehicle_year=profile.vehicle_year,
            license_plate=profile.license_plate,
            stripe_account_id=stripe_account["account_id"]
        )
        
        db.add(driver_profile)
        db.commit()
        db.refresh(driver_profile)
        
        return DriverProfileResponse.from_orm(driver_profile)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/profile", response_model=DriverProfileResponse)
async def get_driver_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get driver profile"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can access driver profiles"
            )
        
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if not driver_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver profile not found"
            )
        
        return DriverProfileResponse.from_orm(driver_profile)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/profile", response_model=DriverProfileResponse)
async def update_driver_profile(
    profile: DriverProfileCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Update driver profile"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can update driver profiles"
            )
        
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if not driver_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver profile not found"
            )
        
        # Update profile fields
        driver_profile.vehicle_make = profile.vehicle_make
        driver_profile.vehicle_model = profile.vehicle_model
        driver_profile.vehicle_year = profile.vehicle_year
        driver_profile.license_plate = profile.license_plate
        
        db.commit()
        db.refresh(driver_profile)
        
        return DriverProfileResponse.from_orm(driver_profile)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/online")
async def go_online(
    location: DriverLocationUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Set driver as online"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can go online"
            )
        
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if not driver_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver profile not found"
            )
        
        # Update profile
        driver_profile.is_online = True
        driver_profile.current_latitude = location.latitude
        driver_profile.current_longitude = location.longitude
        
        db.commit()
        
        # Notify via Socket.IO
        await sio.emit('driver_online', {
            'user_id': current_user.id,
            'latitude': location.latitude,
            'longitude': location.longitude
        })
        
        return {"message": "Driver is now online"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/offline")
async def go_offline(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Set driver as offline"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can go offline"
            )
        
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if not driver_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver profile not found"
            )
        
        # Update profile
        driver_profile.is_online = False
        
        db.commit()
        
        # Notify via Socket.IO
        await sio.emit('driver_offline', {
            'user_id': current_user.id
        })
        
        return {"message": "Driver is now offline"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/location")
async def update_location(
    location: DriverLocationUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Update driver location"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can update location"
            )
        
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if not driver_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver profile not found"
            )
        
        # Update location
        driver_profile.current_latitude = location.latitude
        driver_profile.current_longitude = location.longitude
        
        db.commit()
        
        # Notify via Socket.IO
        await sio.emit('update_location', {
            'user_id': current_user.id,
            'latitude': location.latitude,
            'longitude': location.longitude
        })
        
        return {"message": "Location updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/stripe-connect", response_model=StripeConnectResponse)
async def get_stripe_connect_link(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get Stripe Connect onboarding link"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can access Stripe Connect"
            )
        
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if not driver_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver profile not found"
            )
        
        if not driver_profile.stripe_account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stripe account not created"
            )
        
        # Create account link
        account_link = StripeService.create_account_link(
            account_id=driver_profile.stripe_account_id,
            refresh_url="https://your-app.com/driver/onboarding",
            return_url="https://your-app.com/driver/dashboard"
        )
        
        return StripeConnectResponse(
            account_link=account_link,
            account_id=driver_profile.stripe_account_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
