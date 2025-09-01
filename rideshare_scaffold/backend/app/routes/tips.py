from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Tip, Ride, DriverProfile
from ..schemas import TipRequest, TipResponse
from ..auth import get_current_user
from ..stripe_service import StripeService

router = APIRouter(prefix="/tips", tags=["tips"])

@router.post("/", response_model=TipResponse)
async def create_tip(
    tip_request: TipRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Create a tip for a completed ride"""
    try:
        # Get the ride
        ride = db.query(Ride).filter(Ride.id == tip_request.ride_id).first()
        if not ride:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ride not found"
            )
        
        # Verify ride is completed
        if ride.status.value != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only tip for completed rides"
            )
        
        # Verify user is the rider
        if ride.rider_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the rider can tip for this ride"
            )
        
        # Get driver profile
        driver_profile = db.query(DriverProfile).filter(DriverProfile.user_id == ride.driver_id).first()
        if not driver_profile or not driver_profile.stripe_account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver not available for tips"
            )
        
        # Create tip payment intent
        payment_intent = StripeService.create_tip_payment_intent(
            amount=int(tip_request.amount * 100),  # Convert to cents
            driver_account_id=driver_profile.stripe_account_id,
            metadata={
                "ride_id": str(ride.id),
                "from_user_id": str(current_user.id),
                "to_user_id": str(ride.driver_id),
                "tip_amount": str(tip_request.amount)
            }
        )
        
        # Create tip record
        tip = Tip(
            ride_id=tip_request.ride_id,
            from_user_id=current_user.id,
            to_user_id=ride.driver_id,
            amount=tip_request.amount,
            payment_intent_id=payment_intent["payment_intent_id"]
        )
        
        db.add(tip)
        db.commit()
        db.refresh(tip)
        
        return TipResponse.from_orm(tip)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[TipResponse])
async def get_user_tips(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's tip history"""
    try:
        # Get tips given by user
        tips_given = db.query(Tip).filter(Tip.from_user_id == current_user.id).all()
        
        # Get tips received by user (if driver)
        tips_received = []
        if current_user.role.value == "driver":
            tips_received = db.query(Tip).filter(Tip.to_user_id == current_user.id).all()
        
        all_tips = tips_given + tips_received
        
        return [TipResponse.from_orm(tip) for tip in all_tips]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{tip_id}", response_model=TipResponse)
async def get_tip(tip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get specific tip details"""
    try:
        tip = db.query(Tip).filter(Tip.id == tip_id).first()
        if not tip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tip not found"
            )
        
        # Verify user is involved in the tip
        if current_user.id not in [tip.from_user_id, tip.to_user_id]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this tip"
            )
        
        return TipResponse.from_orm(tip)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
