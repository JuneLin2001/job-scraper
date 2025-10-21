from fastapi import FastAPI
from routers import source

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(source.router)
