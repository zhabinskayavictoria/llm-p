from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

DATABASE_URL = f"sqlite+aiosqlite:///{settings.sqlite_path}"

engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)