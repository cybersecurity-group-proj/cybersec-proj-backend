from typing import List, Optional
from app.db.models import Post 
from app.db.main import db_session
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from sqlmodel import select, and_


class PostRepo:

    async def get_all_posts(self, session: db_session) -> List[PostResponse]:
        statement = select(Post)
        result = await session.execute(statement)
        posts = result.scalars().all()

        return [PostResponse.model_validate(post) for post in posts]
    
    async def get_post(self, post_id: str, session: db_session) -> Optional[PostResponse]:
        statement = select(Post).where(Post.uid == post_id)
        result = await session.execute(statement)
        post = result.scalars().one_or_none()

        return PostResponse.model_validate(post) if post else None
    
    async def create_post(self, post_data: PostCreate, session: db_session) -> PostResponse:
      
        new_post = Post(**post_data.model_dump())
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)

        return PostResponse.model_validate(new_post)
    
    async def update_post(self, post_id: str, post: PostUpdate, session: db_session) -> PostResponse:
        statement = select(Post).where(Post.uid == post_id)
        result = await session.execute(statement)
        post_to_update = result.scalars().one_or_none()

        if not post_to_update:
            return None

        for key, value in post.model_dump(exclude_unset=True).items():
            setattr(post_to_update, key, value) 
            
        

        await session.commit()
        await session.refresh(post_to_update)
        return PostResponse.model_validate(post_to_update)
    
    async def delete_post(self, post_id: str, session: db_session) -> bool:
        statement = select(Post).where(Post.uid == post_id)
        result = await session.execute(statement)
        post_to_delete= result.scalars().one_or_none()
        if not post_to_delete:
            return False
        await session.delete(post_to_delete)
        await session.commit()
        return True
    