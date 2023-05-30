from app.models.core import IDModelMixin, TimestampsMixin, CoreModel

class Production(CoreModel):
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
    
    
class ProductionDBModel(Production,TimestampsMixin):
    ...


NewProduction = Production