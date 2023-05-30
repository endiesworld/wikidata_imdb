import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.apis.cast.crud import fn_create_cast
from app.apis.movie.crud import fn_create_movie
from app.db.repositories import CastsRepository, MoviesRepository

from app.models.domains.cast import NewCast, CastDBModel
from app.models.domains.movie import NewMovie
from app.tests.helpers import fixed_data

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_create_cast


@pytest_asyncio.fixture(scope="class")
def new_cast() -> NewCast:
    return fixed_data.new_cast()

@pytest_asyncio.fixture(scope="class")
def new_movie() -> NewMovie:
    return fixed_data.new_movie()

@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    new_cast: NewCast,
    new_movie: NewMovie,
    movies_repo: MoviesRepository,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE casts CASCADE")
        await db.fetch_one("TRUNCATE TABLE movies CASCADE")

    async def do_setup():
        _ = await fn_create_movie(
            new_movie,
            movies_repo,
        )
        return {"new_cast": new_cast}

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestRegisterCast:
    async def test_setup(self, setup):
        new_cast = setup["new_cast"]

        assert isinstance(new_cast, NewCast)
        
    async def test_register_cast(
        self, 
        app: FastAPI, 
        platform_client: AsyncClient, 
        casts_repo: CastsRepository,
        setup
    ) -> None:
        new_cast = setup["new_cast"]
        
        test_results = await FUNCTION_TO_TEST(
            new_cast,
            casts_repo,
        )
        
        assert isinstance(test_results, CastDBModel)
        assert test_results.imdb_id is not None
        assert test_results.created_at is not None