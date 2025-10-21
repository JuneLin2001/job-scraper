from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
import httpx
from database import SessionLocal
from routers.jobs_utils import save_job_to_db

router = APIRouter(
    prefix="/scrape",
    tags=["scrape"],
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


@router.get("/104", summary="抓取 104 職缺", status_code=status.HTTP_200_OK)
async def scrape_104_jobs(db: db_dependency):
    headers = {"User-Agent": USER_AGENT, "Referer": REFERER}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL_104}{PARAMS_104}", headers=headers)
        jobs_list = response.json().get("data", [])

    saved_jobs = [save_job_to_db(db, job_data, source="104")
                  for job_data in jobs_list]
    return {"count": len(saved_jobs), "jobs": saved_jobs}
