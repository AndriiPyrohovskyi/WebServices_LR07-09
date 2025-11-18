"""
Database connection configuration for PostgreSQL with SQLAlchemy async engine.
"""
import os
import subprocess
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/f1_db")

# Replace postgresql:// with postgresql+asyncpg:// for async support
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for ORM models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency function to get database session.
    Usage in FastAPI endpoints:
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
def run_migrations():
    """
    Run Alembic migrations programmatically.
    This function executes 'alembic upgrade head' to apply all pending migrations.
    
    If DROP_DB_ON_START environment variable is set to 'true',
    it will downgrade to base (drop all tables) and then upgrade again.
    """
    # Get the project root directory (where alembic.ini is located)
    project_root = Path(__file__).parent.parent.parent
    
    # Check if we need to drop database first
    drop_db = os.getenv("DROP_DB_ON_START", "false").lower() == "true"
    
    try:
        if drop_db:
            print("⚠️  DROP_DB_ON_START is enabled - dropping all tables...")
            subprocess.run(
                ["alembic", "downgrade", "base"],
                cwd=project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Database dropped successfully")
        
        print("🔄 Running Alembic migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Migrations applied successfully")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        raise


async def init_db():
    """
    Initialize database - run Alembic migrations.
    This should be called on application startup.
    """
    # Run migrations synchronously
    run_migrations()
    
    # Note: We don't use Base.metadata.create_all() anymore
    # because Alembic handles schema creation


async def close_db():
    """
    Close database connection.
    Should be called on application shutdown.
    """
    await engine.dispose()plication shutdown.
    """
    await engine.dispose()
