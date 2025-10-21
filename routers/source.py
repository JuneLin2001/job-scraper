from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
import httpx
from database import SessionLocal

BASE_URL = "https://www.104.com.tw/jobs/search/api/"
PARAMS = "jobs?area=6001001000%2C6001002000&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&order=15&page=1&pagesize=20&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
REFERER = "https://www.104.com.tw/"


BASE_URL_1111 = "https://www.1111.com.tw/api/v1/search/"
PARAMS_1111 = "jobs/?page=1&fromOffset=0&sortBy=ab&sortOrder=desc&conditionsText=d0|c0|%E6%9C%88%E8%96%AA40000%E4%BB%A5%E4%B8%8A&searchUrl=%2Fsearch%2Fjob?page=1%26d0=140802%252C140804%26c0=100100%252C100200%26sa0=40000%26st=1&jobPositions=140802&jobPositions=140804&regions=100100&regions=100200&salaryType=1&salaryFrom=40000"


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


@router.get("/104")
async def get_source_104():
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": REFERER
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}{PARAMS}", headers=headers)
        data = response.json()
    return data


@router.get("/1111")
async def get_source_1111():
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{BASE_URL_1111}{PARAMS_1111}")
        data = response.json()
    return data
