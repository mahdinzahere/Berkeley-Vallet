import math
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Ride, RideStatus, DriverProfile
from ..schemas import RideRequest, RideQuoteResponse, RideResponse, RideStatusUpdate
from ..auth import get_current_user
from ..stripe_service import StripeService
from ..socket_manager import sio, get_online_drivers
from ..config import settings

router = APIRouter(prefix="/rides", tags=["rides"])

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in miles using Haversine formula"""
    R = 3959  # Earth's radius in miles
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def calculate_fare(distance_miles: float) -> float:
    """Calculate ride fare based on distance"""
    return settings.BASE_FARE + (distance_miles * settings.PER_MILE_RATE)

@router.post("/quote", response_model=RideQuoteResponse)
async def get_ride_quote(request: RideRequest, current_user: User = Depends(get_current_user)):
    """Get ride quote based on pickup and dropoff locations"""
    try:
        # Calculate distance
        distance_miles = calculate_distance(
            request.pickup_latitude, request.pickup_longitude,
            request.dropoff_latitude, request.dropoff_longitude
        )
        
        # Calculate fare
        fare = calculate_fare(distance_miles)
        
        # Estimate time (rough calculation: 1 mile = 2 minutes in city)
        estimated_time_minutes = int(distance_miles * 2)
        
        return RideQuoteResponse(
            fare=fare,
            distance_miles=distance_miles,
            estimated_time_minutes=estimated_time_minutes
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/request", response_model=RideResponse)
async def request_ride(request: RideRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Request a new ride"""
    try:
        # Verify user is a rider
        if current_user.role.value != "rider":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only riders can request rides"
            )
        
        # Calculate fare
        distance_miles = calculate_distance(
            request.pickup_latitude, request.pickup_longitude,
            request.dropoff_latitude, request.dropoff_longitude
        )
        fare = calculate_fare(distance_miles)
        
        # Create ride record
        ride = Ride(
            rider_id=current_user.id,
            pickup_address=request.pickup_address,
            pickup_latitude=request.pickup_latitude,
            pickup_longitude=request.pickup_longitude,
            dropoff_address=request.dropoff_address,
            dropoff_latitude=request.dropoff_latitude,
            dropoff_longitude=request.dropoff_longitude,
            status=RideStatus.REQUESTED,
            fare=fare,
            distance_miles=distance_miles
        )
        
        db.add(ride)
        db.commit()
        db.refresh(ride)
        
        # Broadcast ride request to online drivers via Socket.IO
        await sio.emit('request_ride', {
            'ride_id': ride.id,
            'pickup_latitude': ride.pickup_latitude,
            'pickup_longitude': ride.pickup_longitude,
            'dropoff_latitude': ride.dropoff_latitude,
            'dropoff_longitude': ride.dropoff_longitude,
            'fare': ride.fare
        })
        
        return RideResponse.from_orm(ride)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{ride_id}/accept")
async def accept_ride(ride_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Accept a ride request (driver only)"""
    try:
        # Verify user is a driver
        if current_user.role.value != "driver":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only drivers can accept rides"
            )
        
        # Check if driver has a profile
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == current_user.id).first()
        if not driver_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver profile not found"
            )
        
        # Get ride
        ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if not ride:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ride not found"
            )
        
        if ride.status != RideStatus.REQUESTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ride is not available for acceptance"
            )
        
        # Update ride
        ride.driver_id = current_user.id
        ride.status = RideStatus.ACCEPTED
        
        # Create PaymentIntent with transfer to driver
        if driver_profile.stripe_account_id:
            payment_intent = StripeService.create_payment_intent(
                amount=int(ride.fare * 100),  # Convert to cents
                driver_account_id=driver_profile.stripe_account_id,
                application_fee_amount=0,  # 0% platform fee
                metadata={"ride_id": str(ride.id)}
            )
            ride.payment_intent_id = payment_intent["payment_intent_id"]
        
        db.commit()
        db.refresh(ride)
        
        # Notify via Socket.IO
        await sio.emit('accept_ride', {
            'ride_id': ride.id,
            'driver_id': current_user.id
        })
        
        return {"message": "Ride accepted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{ride_id}/status")
async def update_ride_status(
    ride_id: int, 
    status_update: RideStatusUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Update ride status"""
    try:
        # Get ride
        ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if not ride:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ride not found"
            )
        
        # Verify user is involved in the ride
        if current_user.id not in [ride.rider_id, ride.driver_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this ride"
            )
        
        # Update status
        ride.status = status_update.status
        
        # Handle specific status updates
        if status_update.status == RideStatus.STARTED:
            from datetime import datetime
            ride.started_at = datetime.utcnow()
        elif status_update.status == RideStatus.COMPLETED:
            from datetime import datetime
            ride.completed_at = datetime.utcnow()
            
            # Capture payment if PaymentIntent exists
            if ride.payment_intent_id:
                StripeService.capture_payment_intent(ride.payment_intent_id)
        
        db.commit()
        db.refresh(ride)
        
        # Notify via Socket.IO
        await sio.emit('update_ride_status', {
            'ride_id': ride.id,
            'status': ride.status.value
        })
        
        return {"message": "Ride status updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{ride_id}/cancel")
async def cancel_ride(ride_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Cancel a ride"""
    try:
        # Get ride
        ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if not ride:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ride not found"
            )
        
        # Verify user is involved in the ride
        if current_user.id not in [ride.rider_id, ride.driver_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to cancel this ride"
            )
        
        # Cancel payment if exists
        if ride.payment_intent_id:
            StripeService.cancel_payment_intent(ride.payment_intent_id)
        
        # Update ride status
        ride.status = RideStatus.CANCELLED
        db.commit()
        
        # Notify via Socket.IO
        await sio.emit('update_ride_status', {
            'ride_id': ride.id,
            'status': RideStatus.CANCELLED.value
        })
        
        return {"message": "Ride cancelled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[RideResponse])
async def get_user_rides(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's ride history"""
    try:
        if current_user.role.value == "rider":
            rides = db.query(Ride).filter(Ride.rider_id == current_user.id).all()
        else:
            rides = db.query(Ride).filter(Ride.driver_id == current_user.id).all()
        
        return [RideResponse.from_orm(ride) for ride in rides]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(ride_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get specific ride details"""
    try:
        ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if not ride:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ride not found"
            )
        
        # Verify user is involved in the ride
        if current_user.id not in [ride.rider_id, ride.driver_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this ride"
            )
        
        return RideResponse.from_orm(ride)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
