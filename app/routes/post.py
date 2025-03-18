from fastapi import APIRouter, HTTPException, status , Depends
from typing import List, Annotated
from app.db.main import db_session
from app.repos.post import PostRepo
from app.schemas.post import PostResponse, PostCreate, PostUpdate, PostCreation
from app.auth.dependencies import access_token_bearer, PermissionChecker , get_current_user

post_router = APIRouter()
repo = PostRepo()

create_permission_checker= Annotated[bool,Depends(PermissionChecker(["create posts"]))]
edit_permission_checker= Annotated[bool,Depends(PermissionChecker(["edit own posts","edit posts"]))]
delete_permission_checker= Annotated[bool,Depends(PermissionChecker(["delete posts"]))]

@post_router.get("/", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_all_posts(session: db_session):
    return await repo.get_all_posts(session)

@post_router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: str, session: db_session, user_details: access_token_bearer, ):
    post =  await repo.get_post(post_id, session)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    return post


@post_router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, session: db_session, user_details: access_token_bearer, permission: create_permission_checker, user: get_current_user):
    new_post = PostCreation(
        title=post.title,
        text=post.text,
        user_uid=user.uid
    )

    return await repo.create_post(new_post, session)

@post_router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: str, updated_post : PostUpdate, session: db_session,  user_details: access_token_bearer, permission: edit_permission_checker, user: get_current_user):    
    post = await repo.get_post(post_id, session)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    

    permissions = [permission.name for permission in user.role.permissions]

    if "edit posts" not in permissions:
        if post.author.uid != user.uid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Does not own this post")

    
    return await repo.update_post(post_id, updated_post, session)


@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, session: db_session,  user_details: access_token_bearer, permission: delete_permission_checker):
    deleted = await repo.delete_post(post_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")  
    return 