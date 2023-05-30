import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.review.crud import fn_create_review, fn_get_review_by_imdb
from app.apis.movie.crud import fn_create_movie
from app.db.repositories import ReviewsRepository, MoviesRepository

from app.models.domains.review import NewReview, Review
from app.models.domains.movie import NewMovie
from app.tests.helpers import fixed_data

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_review_by_imdb


@pytest_asyncio.fixture(scope="class")
def new_review() -> NewReview:
    return fixed_data.new_review()

@pytest_asyncio.fixture(scope="class")
def new_movie() -> NewMovie:
    return fixed_data.new_movie()


@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    reviews_repo: ReviewsRepository,
    new_review: NewReview,
    new_movie: NewMovie,
    movies_repo: MoviesRepository,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE reviews CASCADE")
        await db.fetch_one("TRUNCATE TABLE movies CASCADE")

    async def do_setup():
        _ = await fn_create_movie(
            new_movie,
            movies_repo,
        )
        movie_review = await fn_create_review(
            new_review,
            reviews_repo,
        )
        return {
            "new_review": new_review,
            "imdb_id": movie_review.imdb_id,
            }

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestSearchreview:
    async def test_setup(self, setup):
        new_review = setup["new_review"]
        imdb_id = setup["imdb_id"]

        assert isinstance(new_review, NewReview)
        assert isinstance(imdb_id, str)
        
    async def test_search_review(
        self, 
        app: FastAPI, 
        platform_client: AsyncClient, 
        reviews_repo: ReviewsRepository,
        setup
    ) -> None:
        new_review = setup["new_review"]
        imdb_id = setup["imdb_id"]
        
        test_results = await FUNCTION_TO_TEST(
            imdb_id,
            reviews_repo,
        )
        
        assert len(test_results) == 1
        assert isinstance(test_results[0], Review)
        assert test_results[0].imdb_id is not None
        assert test_results[0].rating == new_review.rating