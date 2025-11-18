"""
Repository layer for User CRUD operations.
"""
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User
from src.users.schemas import UserCreate, UserUpdate


class UserRepository:
    """Repository for User database operations."""

    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user."""
        user = User(**user_data.model_dump())
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users with pagination."""
        result = await db.execute(
            select(User)
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> User | None:
        """Get user by username."""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User | None:
        """Update user by ID."""
        # Get existing user
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            return None

        # Update only provided fields
        update_data = user_data.model_dump(exclude_unset=True)
        if not update_data:
            return user

        # Update user
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await db.flush()
        
        # Refresh and return
        await db.refresh(user)
        return user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Delete user by ID."""
        result = await db.execute(delete(User).where(User.id == user_id))
        return result.rowcount > 0
