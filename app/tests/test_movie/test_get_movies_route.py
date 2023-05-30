import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.apis.movie.crud import fn_create_movie
from app.db.repositories import MoviesRepository

from app.models.domains.movie import NewMovie
from app.tests.helpers import fixed_data


pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture(scope="class")
def new_movie() -> NewMovie:
    return fixed_data.new_movie()

@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    new_movie: NewMovie,
    movies_repo: MoviesRepository,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE casts CASCADE")
        await db.fetch_one("TRUNCATE TABLE movies CASCADE")
        await db.fetch_one("TRUNCATE TABLE productions CASCADE")
        await db.fetch_one("TRUNCATE TABLE reviews CASCADE")
        await db.fetch_one("TRUNCATE TABLE genres CASCADE")

    async def do_setup():
        movie = await fn_create_movie(
            new_movie,
            movies_repo,
        )

        return {'movie': movie}
        
    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestGetMovies:
    async def test_setup(self, setup):
        movie = setup["movie"]

        assert movie.imdb_id is not None
        assert movie.created_at is not None
    
    async def test_get_movies(
        self, app: FastAPI, platform_client: AsyncClient, setup
    ) -> None:
        movie = setup["movie"]
        res = await platform_client.get(
            "/movies",
        )
        res_body = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert len(res_body) == 1
        assert res_body[0]['imdb_id'] == movie.imdb_id
        assert res_body[0]['title'] == movie.title