from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Ride, Tip
from ..stripe_service import StripeService
from ..config import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events"""
    try:
        # Get the raw body
        body = await request.body()
        
        # Get the signature from headers
        signature = request.headers.get("stripe-signature")
        if not signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing stripe-signature header"
            )
        
        # Verify webhook signature
        try:
            event = StripeService.verify_webhook_signature(body, signature)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid webhook signature: {str(e)}"
            )
        
        # Handle the event
        event_type = event["type"]
        
        if event_type == "payment_intent.succeeded":
            await handle_payment_intent_succeeded(event["data"]["object"], db)
        elif event_type == "payment_intent.payment_failed":
            await handle_payment_intent_failed(event["data"]["object"], db)
        elif event_type == "account.updated":
            await handle_account_updated(event["data"]["object"], db)
        else:
            # Log unhandled event types
            print(f"Unhandled event type: {event_type}")
        
        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def handle_payment_intent_succeeded(payment_intent: dict, db: Session):
    """Handle successful payment intent"""
    try:
        payment_intent_id = payment_intent["id"]
        metadata = payment_intent.get("metadata", {})
        
        # Check if this is a ride payment
        if "ride_id" in metadata:
            ride_id = metadata["ride_id"]
            ride = db.query(Ride).filter(Ride.id == ride_id).first()
            
            if ride and ride.payment_intent_id == payment_intent_id:
                # Payment succeeded for ride
                print(f"Ride payment succeeded: {ride_id}")
        
        # Check if this is a tip payment
        if "tip_amount" in metadata:
            tip = db.query(Tip).filter(Tip.payment_intent_id == payment_intent_id).first()
            
            if tip:
                # Tip payment succeeded
                print(f"Tip payment succeeded: {tip.id}")
        
    except Exception as e:
        print(f"Error handling payment_intent.succeeded: {str(e)}")

async def handle_payment_intent_failed(payment_intent: dict, db: Session):
    """Handle failed payment intent"""
    try:
        payment_intent_id = payment_intent["id"]
        metadata = payment_intent.get("metadata", {})
        
        # Check if this is a ride payment
        if "ride_id" in metadata:
            ride_id = metadata["ride_id"]
            ride = db.query(Ride).filter(Ride.id == ride_id).first()
            
            if ride and ride.payment_intent_id == payment_intent_id:
                # Payment failed for ride - could update ride status
                print(f"Ride payment failed: {ride_id}")
        
        # Check if this is a tip payment
        if "tip_amount" in metadata:
            tip = db.query(Tip).filter(Tip.payment_intent_id == payment_intent_id).first()
            
            if tip:
                # Tip payment failed - could delete tip record
                print(f"Tip payment failed: {tip.id}")
        
    except Exception as e:
        print(f"Error handling payment_intent.payment_failed: {str(e)}")

async def handle_account_updated(account: dict, db: Session):
    """Handle Stripe Connect account updates"""
    try:
        account_id = account["id"]
        charges_enabled = account.get("charges_enabled", False)
        payouts_enabled = account.get("payouts_enabled", False)
        
        # Update driver profile if account is now fully enabled
        if charges_enabled and payouts_enabled:
            # In a real app, you might want to update a driver's onboarding status
            print(f"Stripe Connect account fully enabled: {account_id}")
        
    except Exception as e:
        print(f"Error handling account.updated: {str(e)}")
