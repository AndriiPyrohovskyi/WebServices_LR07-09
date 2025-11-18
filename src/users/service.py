"""
Service layer for User business logic.
"""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repository import UserRepository
from src.users.schemas import UserCreate, UserUpdate, UserResponse


class UserService:
    """Service for User business logic."""

    def __init__(self):
        self.repository = UserRepository()

    async def create_user(self, db: AsyncSession, user_data: UserCreate) -> UserResponse:
        """Create a new user with validation."""
        # Check if username already exists
        existing_user = await self.repository.get_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{user_data.username}' already exists"
            )

        # Check if email already exists
        existing_email = await self.repository.get_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_data.email}' already registered"
            )

        # Create user
        user = await self.repository.create(db, user_data)
        return UserResponse.model_validate(user)

    async def get_all_users(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        """Get all users."""
        users = await self.repository.get_all(db, skip, limit)
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> UserResponse:
        """Get user by ID."""
        user = await self.repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return UserResponse.model_validate(user)

    async def update_user(self, db: AsyncSession, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update user with validation."""
        # Check if user exists
        existing_user = await self.repository.get_by_id(db, user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )

        # Check username uniqueness if being updated
        if user_data.username and user_data.username != existing_user.username:
            username_check = await self.repository.get_by_username(db, user_data.username)
            if username_check:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Username '{user_data.username}' already exists"
                )

        # Check email uniqueness if being updated
        if user_data.email and user_data.email != existing_user.email:
            email_check = await self.repository.get_by_email(db, user_data.email)
            if email_check:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{user_data.email}' already registered"
                )

        # Update user
        updated_user = await self.repository.update(db, user_id, user_data)
        return UserResponse.model_validate(updated_user)

    async def delete_user(self, db: AsyncSession, user_id: int) -> dict:
        """Delete user."""
        deleted = await self.repository.delete(db, user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return {"message": f"User {user_id} deleted successfully"}
