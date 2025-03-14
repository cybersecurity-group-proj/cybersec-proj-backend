from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

user_role_uid = 0 #get from repo when complete

class UserLogin(BaseModel):
    username: str 
    password: str 

class UserSignUp(BaseModel):
    username: str 
    password: str 
    role_uid: uuid.UUID = user_role_uid

class UserSignUp(BaseModel):
    username: str 
    password: str 
    role_uid: uuid.UUID = user_role_uid

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