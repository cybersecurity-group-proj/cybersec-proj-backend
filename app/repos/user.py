from typing import List, Optional
from app.db.models import User , Role
from app.db.main import db_session
from app.schemas.user import UserResponse, UpdateRole
from sqlmodel import select, and_


class UserRepo:

    async def get_all_users(self, session: db_session) -> List[UserResponse]:
        statement = select(User)
        result = await session.execute(statement)
        users = result.scalars().all()

        return [UserResponse.model_validate(user) for user in users]
    
    async def update_role(self, user_id: str, user: UpdateRole, session: db_session) -> UserResponse:
        statement = select(User).where(User.uid == user_id)
        result = await session.execute(statement)
        user_to_update = result.scalars().one_or_none()

        if not user_to_update:
            return None

        statement = select(Role).where(Role.name == UpdateRole.role)
        result = await session.execute(statement)
        role = result.scalars().one_or_none()

        if not role:
            return None
        
        user_to_update.role = role        

        await session.commit()
        await session.refresh(user_to_update)
        return UserResponse.model_validate(user_to_update)
    
    async def delete_user(self, user_id: str, session: db_session) -> bool:
        statement = select(User).where(User.uid == user_id)
        result = await session.execute(statement)
        user_to_delete= result.scalars().one_or_none()
        if not user_to_delete:
            return False
        await session.delete(user_to_delete)
        await session.commit()
        return True