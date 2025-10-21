from fastapi import FastAPI
from routers import jobs, scrape
import models
from database import engine

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

models.Base.metadata.create_all(bind=engine)


app.include_router(jobs.router)
app.include_router(scrape.router)
