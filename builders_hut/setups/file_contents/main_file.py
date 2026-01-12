from textwrap import dedent

MAIN_FILE_CONTENT = dedent("""
from fastapi import FastAPI


def create_app() -> FastAPI:
    '''
    Create a fastapi app
    '''
    app = FastAPI()

    return app


app = create_app()

""")
