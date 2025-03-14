from pydantic import BaseModel
from typing import Literal
import uuid

class CreatePost(BaseModel):
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

class ResponsePost(BaseModel):
    title: str
    text: str
    author: UserResponse
    
    model_config = {
        "from_attributes": True
    }
