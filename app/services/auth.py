from typing import Optional
from bson import ObjectId
from app.database import get_database
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import get_password_hash, verify_password
from datetime import datetime


async def authenticate_user(email: str, password: str) -> Optional[UserResponse]:
    """Authenticate user with email and password"""
    db = get_database()
    user = await db.users.find_one({"email": email})
    
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        created_at=user["created_at"],
        is_active=user["is_active"]
    )


async def register_user(user_data: UserCreate) -> UserResponse:
    """Register a new user"""
    db = get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Create user document
    user_doc = {
        "_id": ObjectId(),
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": get_password_hash(user_data.password),
        "role": user_data.role,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    await db.users.insert_one(user_doc)
    
    return UserResponse(
        id=str(user_doc["_id"]),
        email=user_doc["email"],
        full_name=user_doc["full_name"],
        role=user_doc["role"],
        created_at=user_doc["created_at"],
        is_active=user_doc["is_active"]
    )
