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
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
REFERER = "https://www.104.com.tw/"


@router.get("/104", summary="抓取 104 職缺", status_code=status.HTTP_200_OK)
async def scrape_104_jobs(db: db_dependency):
    headers = {"User-Agent": USER_AGENT, "Referer": REFERER}
    pagesize = 30
    area = "6001001000%2C6001002000"
    jobcat = "2007001015%2C2007001017"

    saved_jobs = []
    current_page = 1
    total_page = 1

    async with httpx.AsyncClient(verify=False) as client:
        while current_page <= total_page:
            print(f"📄 抓取第 {current_page} 頁...")
            PARAMS_104 = f"jobs?area={area}&jobcat={jobcat}&page={current_page}&pagesize={pagesize}"
            response = await client.get(f"{BASE_URL_104}{PARAMS_104}", headers=headers)
            data = response.json()

            jobs_list = data.get("data", [])

            total_page = data.get("metadata", {}).get(
                "pagination", {}).get("lastPage", 1)

            for job_data in jobs_list:
                job = save_job_to_db(db, job_data, source="104")
                if job:
                    saved_jobs.append(job)

            print(f"✅ 第 {current_page} 頁完成。")

            # if current_page > 10:
            #     break

            current_page += 1

    return {
        "total_saved": len(saved_jobs),
    }
