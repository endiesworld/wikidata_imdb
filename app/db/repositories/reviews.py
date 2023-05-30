from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.review import (
    Review,
    NewReview,
    ReviewDBModel
)

NEW_REVIEW_SQL = """
    INSERT INTO reviews(imdb_id, rating)
    VALUES(:imdb_id, :rating)
    ON CONFLICT (imdb_id, rating) DO NOTHING
    RETURNING *;
"""

GET_REVIEW_IMDB_SQL = """
    SELECT imdb_id, rating FROM reviews WHERE imdb_id = :imdb_id;
"""

class ReviewsRepository(BaseRepository):
    async def create_review(
        self, *, new_review: NewReview
    ) -> ReviewDBModel:
        query_values = new_review.dict()
        
        created_review = await self.db.fetch_one(
            query=NEW_REVIEW_SQL, values=query_values
        )
        return ReviewDBModel(**created_review) if created_review else None
    
    async def get_review_imdb(
        self, *, imdb_id: str
    ) -> List[Review]:
        query_values = {"imdb_id": imdb_id}
        
        reviews = await self.db.fetch_all(
            query=GET_REVIEW_IMDB_SQL, values=query_values
        )
        movie_reviews = [Review(**review) for review in reviews] if reviews else []
        return movie_reviews

    