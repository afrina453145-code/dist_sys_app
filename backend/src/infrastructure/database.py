from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Setup the connection string
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres.xjfstxulsyfqyvxinazg:Afrina453145@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

# 2. Create the engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"ssl": "require"}
)

# 3. Create Session and Base
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 4. The helper function (The one currently missing!)
async def get_db():
    async with SessionLocal() as session:
        yield session