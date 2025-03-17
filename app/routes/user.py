from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.repos.user import UserRepo
from app.schemas.user import UserResponse, UpdateRole
from app.auth.dependencies import access_token_bearer, PermissionChecker


permission_checker= Annotated[bool,Depends(PermissionChecker(["edit users"]))]
user_router = APIRouter()
repo = UserRepo()

@user_router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(session: db_session,   user_details: access_token_bearer, permission: permission_checker):
    return await repo.get_all_users(session)

@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, updated_role : UpdateRole, session: db_session,  user_details: access_token_bearer, permission: permission_checker):    
    user = await repo.get_user(user_id, session)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await repo.update_role(user_id,updated_role,session)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, session: db_session,  user_details: access_token_bearer, permission: permission_checker):
    deleted = await repo.delete_user(user_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")  
    return 
