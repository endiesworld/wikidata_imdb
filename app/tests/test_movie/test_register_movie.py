import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.movie.crud import fn_create_movie
from app.db.repositories import MoviesRepository

from app.models.domains.movie import NewMovie, MovieDBModel
from app.tests.helpers import fixed_data

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_create_movie


@pytest_asyncio.fixture(scope="class")
def new_movie() -> NewMovie:
    return fixed_data.new_movie()


@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    new_movie: NewMovie,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE movies CASCADE")

    async def do_setup():
        return {"new_movie": new_movie}

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestRegisterMovie:
    async def test_setup(self, setup):
        new_movie = setup["new_movie"]

        assert isinstance(new_movie, NewMovie)
        
    async def test_register_movie(
        self, 
        app: FastAPI, 
        platform_client: AsyncClient, 
        movies_repo: MoviesRepository,
        setup
    ) -> None:
        new_movie = setup["new_movie"]
        
        test_results = await FUNCTION_TO_TEST(
            new_movie,
            movies_repo,
        )
        
        assert isinstance(test_results, MovieDBModel)
        assert test_results.imdb_id is not None
        assert test_results.created_at is not None