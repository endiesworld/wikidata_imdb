from typing import Optional

from app.models.core import IDModelMixin
from app.models.exceptions.crud_exception import (
    NotFoundException,
    DuplicateDataException,
)
from app.models.domains.review import NewReview, Review

from app.db.repositories import ReviewsRepository

from . import crud

async def fn_create_review(
    imdb_id: str,
    rating: str,
    reviews_repo: ReviewsRepository,
) -> IDModelMixin:
    
    new_review = NewReview(imdb_id=imdb_id, rating=rating)
    return await crud.fn_create_review( new_review=new_review, reviews_repo=reviews_repo)
    

fn_get_review_by_imdb = crud.fn_get_review_by_imdb