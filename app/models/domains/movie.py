from app.models.core import IDModelMixin, TimestampsMixin

class Movie(TimestampsMixin, IDModelMixin):
    imdb_id: str
    title: str
    cost: int
    icaa_rating: str


class MovieDBModel(Movie):
    id: int


NewMovie = Movie
