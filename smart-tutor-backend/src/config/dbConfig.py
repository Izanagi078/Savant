import os
import re
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load from environment, fallback to SQLite if postgres config isn't ready yet
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smart_tutor.db")

# Helper to format connection strings for asyncpg/aiosqlite
def get_async_db_url(url: str) -> str:
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    
    # Translate sslmode to ssl for asyncpg compatibility
    if "sslmode=" in url:
        url = url.replace("sslmode=require", "ssl=require")
        url = url.replace("sslmode=disable", "ssl=disable")
        url = url.replace("sslmode=prefer", "ssl=prefer")
        url = url.replace("sslmode=allow", "ssl=allow")
    
    # Strip channel_binding since asyncpg doesn't support it
    if "channel_binding=" in url:
        url = re.sub(r'[&?]channel_binding=[^&]+', '', url)
        
    return url

ASYNC_DATABASE_URL = get_async_db_url(DATABASE_URL)

engine = None
# Try connecting to remote async PostgreSQL first
if "asyncpg" in ASYNC_DATABASE_URL:
    try:
        temp_engine = create_async_engine(ASYNC_DATABASE_URL)
        engine = temp_engine
        print("Configured async PostgreSQL connection successfully!")
    except Exception as e:
        print(f"Async PostgreSQL config failed ({e}). Falling back to local SQLite.")
        ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./smart_tutor.db"

if engine is None:
    # Fallback to local async SQLite
    engine = create_async_engine(
        ASYNC_DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in ASYNC_DATABASE_URL else {}
    )
    print("Configured async SQLite connection successfully!")

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

# Async dependency to get db session per request
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
