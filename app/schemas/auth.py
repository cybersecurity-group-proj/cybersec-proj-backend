from pydantic import BaseModel, field_validator
from typing import Optional, List
import uuid


class UserLogin(BaseModel):
    username: str
    password: str
class UserSignUp(BaseModel):
    username: str 
    password: str 
    name:str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one number.")
        if not any(c in "@$!%*?&" for c in password):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return password

class RoleResponse(BaseModel):
    name: str

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    uid: uuid.UUID
    username: str
    name:str
    role: RoleResponse
    model_config = {
        "from_attributes": True
    }