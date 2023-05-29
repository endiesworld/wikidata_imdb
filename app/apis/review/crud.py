from app.models.core import IDModelMixin
from app.models.domains.review import NewReview, Review

from app.db.repositories import ReviewsRepository


async def fn_create_review(
    new_review: NewReview,
    reviews_repo: ReviewsRepository,
) -> IDModelMixin:
    return await reviews_repo.create_review(
        new_review=new_review,
    )
    
async def fn_get_review_by_imdb(
    imdb: str,
    reviews_repo: ReviewsRepository,
) -> Review:
    return await reviews_repo.get_review_imdb(
        imdb=imdb,
    )