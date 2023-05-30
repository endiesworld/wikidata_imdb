from app.models.core import IDModelMixin, TimestampsMixin, CoreModel

class Review(CoreModel):
    imdb_id: str
    rating: str
    
    
class ReviewDBModel(Review,TimestampsMixin):
    ...


NewReview = Review