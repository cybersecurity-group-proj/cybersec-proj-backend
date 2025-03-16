from fastapi.security import HTTPBearer
from typing import Annotated, List
from fastapi import Request, Depends, status
from fastapi.security.http import HTTPAuthorizationCredentials
from app.auth.utils import decode_token
from fastapi.exceptions import HTTPException
from app.db.redis import token_in_blocklist
from app.db.main import db_session
from app.repos.auth import AuthRepo
from app.schemas.auth import UserResponse
from app.db.models import User

user_repo = AuthRepo()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)

        token = credentials.credentials

        token_data = decode_token(token)

        if not self.token_validator(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        self.verify_token_data(token_data)

        return token_data

    def token_validator(self, token: str) -> bool:

        token_data = decode_token(token)

        return True if token_data else False
    

    def verify_token_data(self, token_data):
        raise NotImplementedError("Override method in child class")



class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide a valid access token",
            )

class RefreshTokenBearer(TokenBearer):
     def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide a valid refresh token",
            )


access_token_bearer = Annotated[dict, Depends(AccessTokenBearer())]

refresh_token_bearer = Annotated[dict, Depends(RefreshTokenBearer())]


async def GetCurrentUser(
    token_details: access_token_bearer,
    session: db_session,
):
    username = token_details["user"]["username"]

    user = await user_repo.get_user_by_username(username,session)

    return user

get_current_user = Annotated[User,Depends(GetCurrentUser)]

class RoleChecker:
    def __init__(self, allowed_permissions: List[str]) -> None:
        self.allowed_roles = allowed_permissions

    def __call__(self, current_user: get_current_user):
        
        for permission in current_user.role.permissions:
            if permission.description in self.allowed_permissions:
                return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to preform this action"
        )
