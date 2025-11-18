"""
REST API endpoints for User CRUD operations.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.users.schemas import UserCreate, UserUpdate, UserResponse
from src.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user with the following information:
    - **username**: unique username (3-50 characters)
    - **email**: valid email address (unique)
    - **full_name**: optional full name
    """
    return await user_service.create_user(db, user_data)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Get all users"
)
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all users with pagination:
    - **skip**: number of records to skip (default: 0)
    - **limit**: maximum number of records to return (default: 100)
    """
    return await user_service.get_all_users(db, skip, limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID"
)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific user by their ID.
    """
    return await user_service.get_user_by_id(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update user information by ID:
    - **username**: new username (optional)
    - **email**: new email (optional)
    - **full_name**: new full name (optional)
    - **is_active**: active status (optional)
    """
    return await user_service.update_user(db, user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user"
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a user by their ID.
    """
    return await user_service.delete_user(db, user_id)
