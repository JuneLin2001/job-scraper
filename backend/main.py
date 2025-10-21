from fastapi import FastAPI
from routers import jobs, scrape
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


app.include_router(jobs.router, prefix="/api")
app.include_router(scrape.router, prefix="/api")
