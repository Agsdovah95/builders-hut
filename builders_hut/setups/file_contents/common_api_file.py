from textwrap import dedent

COMMON_API_CONTENT = dedent("""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scalar_fastapi import Theme, get_scalar_api_reference

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/docs", include_in_schema=False)
async def get_docs():
    '''
    Get the documentation for the API
    '''
    return get_scalar_api_reference(
        dark_mode=True,
        show_developer_tools=True,
        hide_download_button=True,
        theme=Theme.PURPLE,
        hide_models=True,
    )
""")
COMMON_API_INIT = dedent("""
from app.api.common import router as common_router

__all__ = ["common_router"]
""")
