from pydantic import BaseModel
from typing import Literal
import uuid

class UpdateRole(BaseModel):
    role: Literal["banned", "user", "moderator", "admin"]


class RoleResponse(BaseModel):
    name: str

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    uid: uuid.UUID
    username: str
    name: str
    role: RoleResponse
    model_config = {
        "from_attributes": True
    }