from sqlmodel import SQLModel, Field, Column, Relationship, DateTime
import uuid
import sqlalchemy.dialects.postgresql as pg
from typing import Optional, List
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ = "app_user"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    username: str = Field(unique=True)
    password_hash: str = Field(exclude=True)

    role_uid: uuid.UUID = Field(foreign_key="role.uid", ondelete="CASCADE") 
    
    role: Optional["Role"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )

class RolePermission(SQLModel, table=True):
    __tablename__ = "rolepermission"

    role_uid: uuid.UUID = Field(foreign_key="role.uid", ondelete="CASCADE", primary_key=True)
    permission_uid: uuid.UUID = Field(foreign_key="permission.uid", ondelete="CASCADE", primary_key=True)

class Role(SQLModel, table=True):
    __tablename__ = "role"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = None

    users: List["User"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    permissions: List["Permission"] = Relationship(
        back_populates="roles",
        link_model=RolePermission,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Permission(SQLModel, table=True):
    __tablename__ = "permission"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    description: Optional[str] = None

    roles: List["Role"] = Relationship(
        back_populates="permissions",
        link_model=RolePermission,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Post(SQLModel, table=True):
    __tablename__ = "post" 

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    title: str
    text: str
    time: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)))

    user_uid: uuid.UUID = Field(foreign_key="app_user.uid", ondelete="CASCADE") 

    author: Optional["User"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )