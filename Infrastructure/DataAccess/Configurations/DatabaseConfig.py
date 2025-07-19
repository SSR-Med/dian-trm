from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import ssl
import certifi

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

REQUIRE_SSL = os.getenv("REQUIRE_SSL", "False").lower() == "true" 

engine_args = {
    "echo": True,
    "future": True
}

if REQUIRE_SSL:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    engine_args["connect_args"] = {"ssl": ssl_context}

engine = create_async_engine(
    DATABASE_URL,
    **engine_args 
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
