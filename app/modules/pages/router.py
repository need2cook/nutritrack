from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

router = APIRouter(tags=['pages'])


@router.get("/")
async def start_page(request: Request):
    return templates.TemplateResponse("start.html", {"request": request})

