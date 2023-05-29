from app.models.core import IDModelMixin, TimestampsMixin

class Production(TimestampsMixin, IDModelMixin):
    imdb_id: str
    director: str
    country: str
    duration: str
    producer: str
    language: str
    distributor: str
    company: str
    cost: int
    date: str
    
    
class ProductionDBModel(Production):
    ...


NewProduction = Production