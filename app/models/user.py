from enum import Enum
from datetime import datetime
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User:
    """User model for MongoDB"""
    
    def __init__(
        self,
        email: str,
        full_name: str,
        hashed_password: str,
        role: UserRole = UserRole.USER,
        _id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        is_active: bool = True
    ):
        self._id = _id
        self.email = email
        self.full_name = full_name
        self.hashed_password = hashed_password
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.is_active = is_active
    
    def to_dict(self):
        return {
            "_id": self._id,
            "email": self.email,
            "full_name": self.full_name,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "created_at": self.created_at,
            "is_active": self.is_active
        }
    
    @staticmethod
    def from_dict(data: dict):
        return User(
            _id=str(data.get("_id")),
            email=data["email"],
            full_name=data["full_name"],
            hashed_password=data["hashed_password"],
            role=data.get("role", UserRole.USER),
            created_at=data.get("created_at"),
            is_active=data.get("is_active", True)
        )
