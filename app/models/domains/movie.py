from app.models.core import IDModelMixin, TimestampsMixin, CoreModel

class Movie(CoreModel):
    imdb_id: str
    title: str
    icaa_rating: str


class MovieDBModel(Movie, TimestampsMixin):
    ...


NewMovie = Movie
