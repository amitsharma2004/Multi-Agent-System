from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user
