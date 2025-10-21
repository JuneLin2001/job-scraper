from fastapi import APIRouter
from . import jobs

router = APIRouter()

router.include_router(jobs.router, prefix="", tags=["jobs"])
