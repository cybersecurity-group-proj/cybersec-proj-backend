from pydantic import BaseModel
from typing import Literal
import uuid

class UpdateRole(BaseModel):
    user_uid: uuid.UUID
    role: Literal["Banned", "User", "Moderator", "Admin"]


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