from fastapi import FastAPI
from routers import source_104

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(source_104.router)
