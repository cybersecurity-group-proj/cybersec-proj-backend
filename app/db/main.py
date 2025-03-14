from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from app.db.config import Config
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import Annotated
from typing import AsyncGenerator

engine : AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    future=True
)
    
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

db_session = Annotated[AsyncSession, Depends(get_async_session)]