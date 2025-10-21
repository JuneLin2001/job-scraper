from fastapi import APIRouter
from . import scrape_104, scrape_1111

router = APIRouter()

router.include_router(scrape_104.router, prefix="", tags=["scrape"])
router.include_router(scrape_1111.router, prefix="", tags=["scrape"])
