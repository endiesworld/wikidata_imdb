from app.models.core import IDModelMixin, TimestampsMixin

class Review(TimestampsMixin, IDModelMixin):
    imdb_id: str
    rating: str
    
    
class ReviewDBModel(Review):
    ...


NewReview = Review