from fastapi import APIRouter
import httpx

BASE_URL = "https://www.104.com.tw/jobs/search/api/"
PARAMS = "jobs?area=6001001000%2C6001002000&jobcat=2007001015%2C2007001017&jobsource=joblist_search&mode=s&order=15&page=1&pagesize=20&scmin=40000&scneg=1&scstrict=1&sctp=M&searchJobs=1"

router = APIRouter(
    prefix="/source_104",
    tags=["source_104"],
)


@router.get("/")
async def get_source_104():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.104.com.tw/"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}{PARAMS}", headers=headers)
        data = response.json()
    return data
