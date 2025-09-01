from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, UserRole
from ..schemas import MagicLinkRequest, VerifyCodeRequest, TokenResponse, UserResponse
from ..auth import send_magic_link, verify_magic_link_code, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/magic-link", response_model=dict)
async def request_magic_link(request: MagicLinkRequest, db: Session = Depends(get_db)):
    """Request magic link for authentication"""
    try:
        # Generate and send verification code
        code = send_magic_link(request.email, request.phone, request.role.value)
        
        # Check if user exists, create if not
        user = db.query(User).filter(
            User.email == request.email,
            User.phone == request.phone
        ).first()
        
        if not user:
            user = User(
                email=request.email,
                phone=request.phone,
                role=request.role,
                is_verified=False
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        return {
            "message": "Verification code sent",
            "code": code  # In production, remove this and send via SMS/email
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/verify", response_model=TokenResponse)
async def verify_code(request: VerifyCodeRequest, db: Session = Depends(get_db)):
    """Verify magic link code and return JWT token"""
    try:
        # Verify the code
        user_data = verify_magic_link_code(request.email, request.phone, request.code)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification code"
            )
        
        # Get or create user
        user = db.query(User).filter(
            User.email == request.email,
            User.phone == request.phone
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Mark user as verified
        user.is_verified = True
        db.commit()
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return TokenResponse(access_token=access_token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's profile"""
    return UserResponse.from_orm(current_user)
