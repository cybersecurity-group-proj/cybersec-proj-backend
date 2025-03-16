from typing import Optional
from app.db.models import User, Role
from app.db.main import db_session
from sqlmodel import select
from app.schemas.auth import UserSignUp, UserResponse
from app.auth.utils import generate_passwd_hash

class AuthRepo:
    
    async def get_user_by_username(self,username: str, session: db_session) -> User:       
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        user = result.scalars().one_or_none()
        return user
    
    async def user_exists(self, session: db_session,username :Optional[str] = None,) -> bool:
        
        if not username:
            raise ValueError("Either email or username must be provided")

        statement = select(User).where(User.username == username)

        result = await session.execute(statement)
        user = result.scalars().one_or_none()

        return user is not None
    
    async def create_user(self, user_data: UserSignUp, session: db_session) -> UserResponse:
      
        new_user = User(**user_data.model_dump())
        new_user.password_hash = generate_passwd_hash(user_data.password)
        user_role = await session.execute(select(Role).where(Role.name == "user"))
        new_user.role = user_role.scalars().one_or_none()

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return UserResponse.model_validate(new_user)