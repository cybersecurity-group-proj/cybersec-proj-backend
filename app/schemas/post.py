from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime
class PostCreate(BaseModel):
    title: str
    text: str

class PostCreation(PostCreate):
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
    uid: uuid.UUID
    title: str
    text: str
    time: datetime

    author: UserResponse
    
    model_config = {
        "from_attributes": True
    }


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    