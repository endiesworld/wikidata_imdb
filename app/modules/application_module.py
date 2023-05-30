from typing import Callable

from fastapi import FastAPI


def mount(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import (
            home_page, 
            query_wikidata,
            movies_route,
        )
            
        
        app.include_router( home_page.router )
        app.include_router( query_wikidata.router )
        app.include_router( movies_route.router )
        
    return start_app
