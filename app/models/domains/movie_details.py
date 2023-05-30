from typing import List, Optional


from app.models.domains.cast import Cast
from app.models.domains.movie import Movie
from app.models.domains.genre import Genre
from app.models.domains.production import Production
from app.models.domains.review import Review

class MovieDetails(Movie):
    genre:List[Genre]
    production: List[Production]
    review: List[Review]
    cast: Optional[Cast]
    
    
