from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from models import Job

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


@router.get("/", summary="查看所有職缺", status_code=status.HTTP_200_OK)
def get_all_jobs(db: db_dependency):
    jobs = db.query(Job).all()
    number_of_jobs = len(jobs)
    return {"count": number_of_jobs, "jobs": jobs}


@router.get("/104", summary="查看已存 104 職缺", status_code=status.HTTP_200_OK)
def get_104_jobs(db: db_dependency):
    jobs = db.query(Job).filter(Job.source == "104").all()
    return jobs


@router.get("/1111", summary="查看已存 1111 職缺", status_code=status.HTTP_200_OK)
def get_1111_jobs(db: db_dependency):
    jobs = db.query(Job).filter(Job.source == "1111").all()
    return jobs
