from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import UserLoginRequest, LoginResponse, UserResponse
from app.services.user_service import verify_user_credentials

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLoginRequest):
    """Login user dan mendapatkan JWT token"""
    user = await verify_user_credentials(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Buat access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user["_id"])},
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(**user)
    )


@router.post("/logout")
async def logout(current_user: dict = None):
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}
