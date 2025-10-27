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

BASE_URL_1111 = "https://www.1111.com.tw/api/v1/search/"
PARAMS_1111 = "jobs/?page={page}&fromOffset=0&sortBy=ab&sortOrder=desc&conditionsText=d0|c0|%E6%9C%88%E8%96%AA40000%E4%BB%A5%E4%B8%8A&searchUrl=%2Fsearch%2Fjob?page={page}%26d0=140802%252C140804%26c0=100100%252C100200%26sa0=40000%26st=1&jobPositions=140802&jobPositions=140804&regions=100100&regions=100200&salaryType=1&salaryFrom=40000"


@router.get("/1111", summary="抓取 1111 全部分頁職缺", status_code=status.HTTP_200_OK)
async def scrape_1111_jobs(db: db_dependency):
    async with httpx.AsyncClient(verify=False) as client:
        page = 1
        total_pages = 1
        saved_jobs = []

        while page <= total_pages:
            print(f"📄 抓取第 {page} 頁...")
            response = await client.get(f"{BASE_URL_1111}{PARAMS_1111.format(page=page)}")
            data = response.json()
            result = data.get("result", {})

            total_pages = result.get("pagination", {}).get("totalPage", 1)
            jobs_list = result.get("hits", [])

            for job_data in jobs_list:
                job = save_job_to_db(db, job_data, source="1111")
                if job:
                    saved_jobs.append(job)

            page += 1

    return {"total_saved": len(saved_jobs)}
