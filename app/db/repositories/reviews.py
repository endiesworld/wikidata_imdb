from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.review import (
    Review,
    NewReview,
)

NEW_REVIEW_SQL = """
    INSERT INTO reviews(imdb_id, rating)
    VALUES(:imdb_id, :rating)
    ON CONFLICT (imdb_id, rating) DO NOTHING
    RETURNING id;
"""

GET_REVIEW_IMDB_SQL = """
    SELECT rating FROM reviews WHERE imdb_id = :imdb_id;
"""

class ReviewsRepository(BaseRepository):
    async def create_review(
        self, *, new_review: NewReview
    ) -> IDModelMixin:
        query_values = new_review.dict()
        
        created_review = await self.db.fetch_one(
            query=NEW_REVIEW_SQL, values=query_values
        )
        return IDModelMixin(**created_review)
    
    async def get_review_imdb(
        self, *, imdb: str
    ) -> Review:
        query_values = {"imdb": imdb}
        
        review = await self.db.fetch_one(
            query=GET_REVIEW_IMDB_SQL, values=query_values
        )
        return Review(**review)

    