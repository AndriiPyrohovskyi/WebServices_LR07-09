"""
Cache management endpoints for Redis operations.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from redis.asyncio import Redis

from ..cache import get_redis

router = APIRouter(prefix="/cache", tags=["Cache"])


class CacheSetRequest(BaseModel):
    """Request model for setting cache value."""
    key: str = Field(..., description="Cache key", min_length=1, max_length=256)
    value: str = Field(..., description="Cache value", min_length=1)
    ttl: Optional[int] = Field(None, description="Time to live in seconds (optional)", ge=1)


class CacheSetResponse(BaseModel):
    """Response model for set operation."""
    success: bool
    key: str
    message: str
    ttl: Optional[int] = None


class CacheGetResponse(BaseModel):
    """Response model for get operation."""
    key: str
    value: Optional[str]
    exists: bool


@router.post("/set", response_model=CacheSetResponse, status_code=status.HTTP_201_CREATED)
async def set_cache_value(
    data: CacheSetRequest,
    redis: Redis = Depends(get_redis)
) -> CacheSetResponse:
    """
    Set a value in Redis cache with optional TTL.
    
    - **key**: Cache key (1-256 characters)
    - **value**: Value to store
    - **ttl**: Optional time to live in seconds
    """
    try:
        if data.ttl:
            await redis.setex(data.key, data.ttl, data.value)
            message = f"Value set with TTL of {data.ttl} seconds"
        else:
            await redis.set(data.key, data.value)
            message = "Value set without expiration"
        
        return CacheSetResponse(
            success=True,
            key=data.key,
            message=message,
            ttl=data.ttl
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set cache value: {str(e)}"
        )


@router.get("/get/{key}", response_model=CacheGetResponse)
async def get_cache_value(
    key: str,
    redis: Redis = Depends(get_redis)
) -> CacheGetResponse:
    """
    Get a value from Redis cache by key.
    
    - **key**: Cache key to retrieve
    """
    try:
        value = await redis.get(key)
        
        return CacheGetResponse(
            key=key,
            value=value,
            exists=value is not None
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cache value: {str(e)}"
        )


@router.delete("/delete/{key}")
async def delete_cache_value(
    key: str,
    redis: Redis = Depends(get_redis)
):
    """
    Delete a value from Redis cache.
    
    - **key**: Cache key to delete
    """
    try:
        deleted_count = await redis.delete(key)
        
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Key '{key}' not found in cache"
            )
        
        return {
            "success": True,
            "key": key,
            "message": "Key deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete cache value: {str(e)}"
        )


@router.get("/keys")
async def list_cache_keys(
    pattern: str = "*",
    redis: Redis = Depends(get_redis)
):
    """
    List all keys matching a pattern.
    
    - **pattern**: Key pattern (default: * for all keys)
    """
    try:
        keys = await redis.keys(pattern)
        
        return {
            "pattern": pattern,
            "count": len(keys),
            "keys": keys
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list cache keys: {str(e)}"
        )
