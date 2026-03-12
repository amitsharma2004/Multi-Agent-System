from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.database import get_database
from app.utils.security import decode_access_token
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_token_from_cookie_or_header(
    request: Request,
    token_from_header: Optional[str] = Depends(oauth2_scheme)
) -> Optional[str]:
    """
    Extract token from cookie first, then fall back to Authorization header
    Priority: Cookie > Bearer Token
    """
    # First, try to get token from cookie
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        print(f"🍪 Token from cookie: {cookie_token[:50]}...")
        # Remove "Bearer " prefix if present
        if cookie_token.startswith("Bearer "):
            return cookie_token[7:]
        return cookie_token
    
    # Fall back to Authorization header
    if token_from_header:
        print(f"🔑 Token from header: {token_from_header[:50]}...")
        return token_from_header
    
    print("❌ No token found in cookie or header")
    return None


async def get_current_user(
    token: Optional[str] = Depends(get_token_from_cookie_or_header)
) -> UserResponse:
    """Get current authenticated user from cookie or bearer token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    email = decode_access_token(token)
    if email is None:
        raise credentials_exception
    
    db = get_database()
    user = await db.users.find_one({"email": email})
    
    if user is None:
        raise credentials_exception
    
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        created_at=user["created_at"],
        is_active=user["is_active"]
    )


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
