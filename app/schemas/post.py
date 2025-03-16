from pydantic import BaseModel
from typing import Optional
import uuid

class PostCreate(BaseModel):
    title: str
    text: str
    user_uid: uuid.UUID

class RoleResponse(BaseModel):
    name: str

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    uid: uuid.UUID
    username: str
    role: RoleResponse

    model_config = {
        "from_attributes": True
    }

class PostResponse(BaseModel):
    title: str
    text: str
    author: UserResponse
    
    model_config = {
        "from_attributes": True
    }


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    