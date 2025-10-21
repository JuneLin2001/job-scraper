from fastapi import FastAPI
from routers import source
import models
from database import engine

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

models.Base.metadata.create_all(bind=engine)


app.include_router(source.router)
