from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.external_api import router as external_router

app = FastAPI(
    title="F1 Data API",
    description="FastAPI application with Formula 1 data integration using Ergast API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include F1 API router
app.include_router(external_router.router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - returns API information and available endpoints.
    """
    return {
        "message": "Welcome to F1 Data API",
        "version": "1.0.0",
        "description": "Integration with Ergast F1 API for Formula 1 data",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "raw_data": {
                "drivers": "/external/data/drivers",
                "races": "/external/data/races",
                "standings": "/external/data/standings?season=current",
            },
            "processed_data": {
                "drivers": "/external/processed/drivers",
                "races": "/external/processed/races",
                "standings": "/external/processed/standings?season=current",
            },
            "html_view": "/external/f1/html?season=current",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy", "service": "F1 Data API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
