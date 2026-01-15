from textwrap import dedent

MAIN_FILE_CONTENT = dedent("""

from fastapi import FastAPI
from app.core.config import settings
from app.api import common_router

def create_app() -> FastAPI:
    '''
    Create a fastapi app
    '''
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )

    app.include_router(common_router)

    return app


app = create_app()


""")
