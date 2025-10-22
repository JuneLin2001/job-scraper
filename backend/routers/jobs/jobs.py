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


@router.get("/", status_code=status.HTTP_200_OK)
def get_jobs_paginated(
    db: db_dependency,
    source: str | None = Query(None, description="職缺來源"),
    page: int = Query(1, ge=1, description="頁碼"),
    pagesize: int = Query(30, ge=1, le=100, description="每頁數量")
):
    query = db.query(Job)

    if source:
        if source not in VALID_SOURCES:
            raise HTTPException(
                status_code=400, detail=f"Source must be one of {VALID_SOURCES}"
            )
        query = query.filter(Job.source == source)

    total = query.count()
    jobs = query.offset((page - 1) * pagesize).limit(pagesize).all()

    job_list = []
    for job in jobs:
        job_list.append({
            "id": job.id,
            "jobNo": job.jobNo,
            "title": job.title,
            "description": job.description,
            "company_name": job.company_name,
            "location": job.location,
            "salary": job.salary,
            "updated_at": job.updated_at,
            "link": job.link,
            "source": job.source,
            "labels": [label.name for label in job.labels]
        })

    return {
        "page": page,
        "pagesize": pagesize,
        "count": len(jobs),
        "jobs": job_list,
        "total": total,
        "total_pages": (total + pagesize - 1) // pagesize
    }


@router.delete("/", summary="清空職缺", status_code=status.HTTP_204_NO_CONTENT)
def reset_all_jobs(db: db_dependency):
    db.query(Job).delete()
    db.commit()
