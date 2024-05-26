from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

session = async_session()
Base = declarative_base()
