from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
import httpx
from database import SessionLocal
from models import Job
from starlette import status


router = APIRouter(
    prefix="/source",
    tags=["source"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

BASE_URL_104 = "https://www.104.com.tw/jobs/search/api/"
PARAMS_104 = "jobs?area=6001001000%2C6001002000&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&order=15&page=1&pagesize=20&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
REFERER = "https://www.104.com.tw/"

BASE_URL_1111 = "https://www.1111.com.tw/api/v1/search/"
PARAMS_1111 = "jobs/?page=1&fromOffset=0&sortBy=ab&sortOrder=desc&conditionsText=d0|c0|%E6%9C%88%E8%96%AA40000%E4%BB%A5%E4%B8%8A"


def save_job_to_db(db: Session, job_data, source: str):
    existing_job = db.query(Job).filter(
        Job.jobNo == job_data.get("jobNo")).first()
    if existing_job:
        return existing_job

    job = Job(
        jobNo=job_data.get("jobNo"),
        source=source,
        title=job_data.get("title"),
        description=job_data.get("description"),
        salary=job_data.get("salary"),
        company_name=job_data.get("company_name"),
        location=job_data.get("location"),
        link=job_data.get("link")
    )

    job.labels = []

    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/104", status_code=status.HTTP_200_OK)
async def get_source_104(db: db_dependency):
    headers = {"User-Agent": USER_AGENT, "Referer": REFERER}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL_104}{PARAMS_104}", headers=headers)
        data = response.json()

    jobs_list = data.get("data", [])
    saved_jobs = []
    for item in jobs_list:
        job_data = {
            "jobNo": item.get("jobNo"),
            "title": item.get("jobName"),
            "description": item.get("descSnippet"),
            "salary": f"{item.get('salaryLow')}-{item.get('salaryHigh')}",
            "company_name": item.get("custName"),
            "location": item.get("jobAddress"),
            "link": item.get("link", {}).get("job"),
            "labels": []
        }
        saved_jobs.append(save_job_to_db(db, job_data, source="104"))

    return {"saved": len(saved_jobs), "jobs": [j.title for j in saved_jobs]}


@router.get("/1111", status_code=status.HTTP_200_OK)
async def get_source_1111(db: db_dependency):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{BASE_URL_1111}{PARAMS_1111}")
        data = response.json()

    jobs_list = data.get("result", {}).get("hits", [])
    saved_jobs = []
    for item in jobs_list:
        job_data = {
            "jobNo": str(item.get("jobId")),
            "title": item.get("title"),
            "description": item.get("description"),
            "salary": item.get("salary"),
            "company_name": item.get("companyName"),
            "location": item.get("workCity", {}).get("name"),
            "link": f"https://www.1111.com.tw/job/{item.get('jobId')}",
            "labels": []
        }
        saved_jobs.append(save_job_to_db(db, job_data, source="1111"))

    return {"saved": len(saved_jobs), "jobs": [j.title for j in saved_jobs]}
