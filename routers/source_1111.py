from fastapi import APIRouter
import httpx

BASE_URL = "https://www.1111.com.tw/api/v1/search/"
PARAMS = "jobs/?page=1&fromOffset=0&sortBy=ab&sortOrder=desc&conditionsText=d0|c0|%E6%9C%88%E8%96%AA40000%E4%BB%A5%E4%B8%8A&searchUrl=%2Fsearch%2Fjob?page=1%26d0=140802%252C140804%26c0=100100%252C100200%26sa0=40000%26st=1&jobPositions=140802&jobPositions=140804&regions=100100&regions=100200&salaryType=1&salaryFrom=40000"

router = APIRouter(
    prefix="/source_1111",
    tags=["source_1111"],
)


@router.get("/")
async def get_source_1111():
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{BASE_URL}{PARAMS}")
        data = response.json()
    return data
