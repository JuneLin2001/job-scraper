from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from models import Job
from config import VALID_SOURCES

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", summary="取得職缺", status_code=status.HTTP_200_OK)
def get_jobs(db: db_dependency, source: str | None = Query(None, description="職缺來源")):
    query = db.query(Job)
    if source:
        if source not in VALID_SOURCES:
            raise HTTPException(
                status_code=400, detail=f"Source must be one of {VALID_SOURCES}"
            )
        query = query.filter(Job.source == source)
    jobs = query.all()
    return {"count": len(jobs), "jobs": jobs}
