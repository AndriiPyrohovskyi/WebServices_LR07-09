from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.external_api import router as external_router
from src.users import router as users_router
from src.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for database connection.
    """
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database connection
    await close_db()


app = FastAPI(
    title="F1 Data API",
    description="FastAPI application with Formula 1 data integration, PostgreSQL and Redis caching",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(external_router.router)
app.include_router(users_router.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - returns API information and available endpoints.
    """
    return {
        "message": "Welcome to F1 Data API",
        "version": "2.0.0",
        "description": "Integration with Ergast F1 API, PostgreSQL and Redis",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "f1_raw_data": {
                "drivers": "/external/data/drivers",
                "races": "/external/data/races",
                "standings": "/external/data/standings?season=current",
            },
            "f1_processed_data": {
                "drivers": "/external/processed/drivers",
                "races": "/external/processed/races",
                "standings": "/external/processed/standings?season=current",
            },
            "f1_html_view": "/external/f1/html?season=current",
            "users_crud": {
                "create": "POST /users/",
                "get_all": "GET /users/",
                "get_by_id": "GET /users/{user_id}",
                "update": "PUT /users/{user_id}",
                "delete": "DELETE /users/{user_id}",
            },
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy", "service": "F1 Data API"}


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
