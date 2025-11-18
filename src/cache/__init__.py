"""
Redis cache connection configuration.
"""
import os
from typing import Optional
import redis.asyncio as aioredis
from redis.asyncio import Redis

# Get REDIS_URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Global Redis client
redis_client: Optional[Redis] = None


async def get_redis() -> Redis:
    """
    Dependency function to get Redis client.
    Usage in FastAPI endpoints:
        async def endpoint(redis: Redis = Depends(get_redis)):
            ...
    """
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call init_redis() first.")
    return redis_client


async def init_redis():
    """
    Initialize Redis connection.
    This should be called on application startup.
    """
    global redis_client
    
    try:
        print("🔄 Connecting to Redis...")
        redis_client = await aioredis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
        )
        
        # Test connection
        await redis_client.ping()
        print("✅ Redis connected successfully")
        
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("⚠️  Application will continue without Redis cache")
        redis_client = None


async def close_redis():
    """
    Close Redis connection.
    Should be called on application shutdown.
    """
    global redis_client
    
    if redis_client:
        try:
            await redis_client.aclose()
            print("✅ Redis connection closed")
        except Exception as e:
            print(f"⚠️  Error closing Redis: {e}")
        finally:
            redis_client = None
