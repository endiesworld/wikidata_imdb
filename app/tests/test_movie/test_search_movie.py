import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.movie.crud import fn_create_movie, fn_get_movie_by_imdb
from app.db.repositories import MoviesRepository

from app.models.domains.movie import NewMovie, Movie
from app.tests.helpers import fixed_data

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_movie_by_imdb


@pytest_asyncio.fixture(scope="class")
def new_movie() -> NewMovie:
    return fixed_data.new_movie()


@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    movies_repo: MoviesRepository,
    new_movie: NewMovie,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE movies CASCADE")

    async def do_setup():
        movie_movie = await fn_create_movie(
            new_movie,
            movies_repo,
        )
        return {
            "new_movie": new_movie,
            "imdb_id": movie_movie.imdb_id,
            }

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestSearchMovie:
    async def test_setup(self, setup):
        new_movie = setup["new_movie"]
        imdb_id = setup["imdb_id"]

        assert isinstance(new_movie, NewMovie)
        assert isinstance(imdb_id, str)
        
    async def test_search_movie(
        self, 
        app: FastAPI, 
        platform_client: AsyncClient, 
        movies_repo: MoviesRepository,
        setup
    ) -> None:
        new_movie = setup["new_movie"]
        imdb_id = setup["imdb_id"]
        
        test_results = await FUNCTION_TO_TEST(
            imdb_id,
            movies_repo,
        )
        
        assert isinstance(test_results, Movie)
        assert test_results.imdb_id is not None
        assert test_results.title == new_movie.title