from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import session
from database import get_db
from models import User, Permission



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password(password: str):
    return pwd_context.hash(password)

def verify_password(original_password: str, hashed_password: str):
    return pwd_context.verify(original_password, hashed_password)


class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    def __call__(self, current_user: User = Depends(get_current_user)):
        user_permissions = [p.title for p in current_user.role.permissions]
        if self.required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permission"
            )
        return True