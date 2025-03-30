from app.db.main import async_session
from app.db.models import Permission, User, Role
from app.auth.utils import generate_passwd_hash
import asyncio

#To run: python -m app.db.initialize_db


async def initialize_db():
    async with async_session() as session:
            async with session.begin():

                create_posts_permission = Permission(
                     description="create posts"
                )

                edit_own_posts_permission = Permission(
                     description="edit own posts"
                )

                edit_posts_permission = Permission(
                     description="edit posts"
                )

                delete_posts_permission = Permission(
                     description="delete posts"
                )

                edit_users_permission = Permission(
                     description="edit users"
                )


                session.add(create_posts_permission)
                session.add(edit_own_posts_permission)
                session.add(edit_posts_permission)
                session.add(edit_users_permission)
                session.add(delete_posts_permission)

                await session.flush()  
                await session.refresh(create_posts_permission)
                await session.refresh(edit_own_posts_permission)
                await session.refresh(edit_posts_permission)
                await session.refresh(edit_users_permission)
                await session.refresh(delete_posts_permission)

                user_role = Role(
                     name="user",
                     permissions=[create_posts_permission,edit_own_posts_permission]
                )

                moderator_role = Role(
                     name="moderator",
                     permissions=[delete_posts_permission] + user_role.permissions
                )

                admin_role = Role(
                     name="admin", 
                     permissions=[edit_users_permission,edit_posts_permission] + moderator_role.permissions
                )

                banned_role = Role(
                     name="banned"
                )

                session.add(banned_role)
                session.add(user_role)
                session.add(moderator_role)
                session.add(admin_role)

                await session.flush()
                await session.refresh(admin_role)

                admin_user = User(
                    username="admin",
                    password_hash=generate_passwd_hash("Admin@1234"),
                    role=admin_role,
                    name="admin"

                )

                session.add(admin_user)
                await session.flush()  
                await session.refresh(admin_user) 

                
                await session.commit()


                print("Admin user and permissions initialized successfully.")


if __name__ == "__main__":
    asyncio.run(initialize_db())