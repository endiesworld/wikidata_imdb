import asyncio
import warnings

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient


from app.db.repositories import (
    MoviesRepository,
    CastsRepository,
    GenresRepository,
    ProductionsRepository,
    ReviewsRepository,
)

from app.modules.users.database import User

from . import seed


@pytest_asyncio.fixture
def platform_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


@pytest_asyncio.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # os.environ["TEST"] = "1"
    config = Config("/app/alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    # alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest_asyncio.fixture(scope="session")
def app(apply_migrations: None) -> FastAPI:
    from app.main import app
    return app


@pytest_asyncio.fixture(scope="session")
def db(app: FastAPI) -> Database:
    return app.state.db


# HTTP Test Client
@pytest_asyncio.fixture(scope="session")
async def platform_client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://localhost:5000",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        ) as client:
            yield client


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def movies_repo(db: Database) -> MoviesRepository:
    return MoviesRepository(db)


@pytest_asyncio.fixture(scope="session")
async def casts_repo(db: Database) -> CastsRepository:
    return CastsRepository(db)


@pytest_asyncio.fixture(scope="session")
async def genres_repo(
    db: Database,
) -> GenresRepository:
    return GenresRepository(db)


@pytest_asyncio.fixture(scope="session")
async def productions_repo(
    db: Database,
) -> ProductionsRepository:
    return ProductionsRepository(db)


@pytest_asyncio.fixture(scope="session")
async def reviews_repo(db: Database) -> ReviewsRepository:
    return ReviewsRepository(db)

