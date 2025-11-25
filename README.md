# F1 Data API - LR07-09

FastAPI application with Formula 1 data integration, PostgreSQL database, and Redis caching.

## Features

- 🏎️ **F1 API Integration**: Real-time Formula 1 data from Ergast API
- 🗄️ **PostgreSQL Database**: User management with async SQLAlchemy
- 🚀 **Redis Cache**: High-performance caching layer
- 🔄 **Auto Migrations**: Automatic Alembic migrations on startup
- 🐳 **Docker Ready**: Docker Compose for local development
- ☁️ **Railway Deployment**: Production deployment on Railway

## Tech Stack

- **FastAPI** 0.115.0 - Modern Python web framework
- **SQLAlchemy** 2.0.35 - Async ORM for PostgreSQL
- **Alembic** 1.14.0 - Database migrations
- **Redis** 5.0.1 - In-memory cache
- **asyncpg** 0.30.0 - Async PostgreSQL driver
- **Pydantic** 2.9.0 - Data validation
- **Uvicorn** 0.32.0 - ASGI server

## Local Development

### Option 1: Docker Compose (Recommended)

```bash
# Start all services (PostgreSQL, Redis, FastAPI)
docker-compose up --build

# Access the API
open http://localhost:8080/docs
```

### Option 2: Manual Setup

1. **Start PostgreSQL and Redis**:
```bash
# PostgreSQL
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=f1_db \
  postgres:15-alpine

# Redis
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

2. **Setup Python environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.local .env
```

4. **Run the application**:
```bash
python start.py
```

5. **Access the API**:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## API Endpoints

### F1 Data (External API)
- `GET /external/data/drivers` - Raw drivers data
- `GET /external/data/races` - Raw races data
- `GET /external/data/standings?season=current` - Raw standings
- `GET /external/processed/drivers` - Processed drivers data
- `GET /external/processed/races` - Processed races data
- `GET /external/processed/standings?season=current` - Processed standings
- `GET /external/f1/html?season=current` - HTML view

### Users CRUD (PostgreSQL)
- `POST /users/` - Create user
- `GET /users/` - List users (with pagination)
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Cache Management (Redis)
- `POST /cache/set` - Set cache value with optional TTL
- `GET /cache/get/{key}` - Get cache value
- `DELETE /cache/delete/{key}` - Delete cache key
- `GET /cache/keys?pattern=*` - List cache keys

## Database Migrations

Migrations run automatically on startup. To control:

```bash
# Reset database on startup (CAUTION!)
export DROP_DB_ON_START=true

# Manual migration commands
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1
```

## Environment Variables

Key variables (see `.env.example` for full list):

```bash
# Server
PORT=8080

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
DROP_DB_ON_START=false  # Set to 'true' to reset DB on restart

# Redis
REDIS_URL=redis://host:6379/0

# F1 API
ERGAST_API_BASE_URL=https://api.jolpi.ca/ergast/f1
```

## Railway Deployment

The application is configured for automatic deployment on Railway:

1. Connect your GitHub repository
2. Add the following services:
   - PostgreSQL database
   - Redis instance
3. Set environment variables (Railway provides DATABASE_URL and REDIS_URL automatically)
4. Deploy!

Railway will automatically:
- Build the Docker image
- Run database migrations
- Start the application

## Project Structure

```
LR07-09/
├── alembic/              # Database migrations
├── src/
│   ├── cache/           # Redis cache module
│   │   ├── __init__.py  # Redis connection
│   │   └── router.py    # Cache endpoints
│   ├── database/        # Database configuration
│   │   ├── __init__.py  # SQLAlchemy setup
│   │   └── models.py    # ORM models
│   ├── external_api/    # F1 API integration
│   ├── users/           # Users CRUD
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── router.py
│   └── main.py          # FastAPI application
├── docker-compose.yml   # Local development setup
├── Dockerfile          # Production container
├── requirements.txt    # Python dependencies
└── start.py           # Application entry point
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Test specific endpoint
curl http://localhost:8080/health
```

## Authors

- Andriy Pyrohovskyi

## License

Educational project for Web Services course (LR07-09)
