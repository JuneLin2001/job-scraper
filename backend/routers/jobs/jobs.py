from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from database import SessionLocal
from models import Job, Label
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
def get_jobs(
    db: db_dependency,
    source: str | None = Query(None, description="職缺來源"),
    page: int = Query(1, ge=1, description="頁碼"),
    pagesize: int = Query(30, ge=1, le=100, description="每頁數量"),
    search: str | None = Query(None, description="搜尋關鍵字"),
    labels: str | None = Query(None, description="以逗號分隔標籤篩選")
):
    query = db.query(Job).options(joinedload(Job.labels))

    if source:
        if source not in VALID_SOURCES:
            raise HTTPException(
                status_code=400, detail=f"Source must be one of {VALID_SOURCES}"
            )
        query = query.filter(Job.source.like(f'%"{source}"%'))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Job.title.ilike(search_pattern),
                Job.company_name.ilike(search_pattern),
                Job.description.ilike(search_pattern)
            )
        )

    if labels:
        label_list = [l.strip() for l in labels.split(",") if l.strip()]
        if label_list:
            query = query.filter(Job.labels.any(Label.name.in_(label_list)))

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
            "links": job.links,
            "source": job.source,
            "labels": [label.name for label in job.labels]
        })

    return {
        "total": total,
        "total_pages": (total + pagesize - 1) // pagesize,
        "jobs": job_list,
    }


@router.get("/labels", status_code=status.HTTP_200_OK)
def get_all_labels(db: db_dependency):
    labels = db.query(Label).all()
    return {"labels": [label.name for label in labels]}


@router.get("/both", summary="找出 104 和 1111 皆有的職缺")
def get_jobs_in_both_sources(db: db_dependency):
    jobs = db.query(Job).filter(
        Job.source.like('%"104"%'),
        Job.source.like('%"1111"%')
    ).all()

    return {
        "count": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company_name": job.company_name,
                "source": job.source,
            }
            for job in jobs
        ]
    }


@router.delete("/", summary="清空職缺", status_code=status.HTTP_204_NO_CONTENT)
def reset_all_jobs(db: db_dependency):
    db.query(Job).delete()
    db.commit()
