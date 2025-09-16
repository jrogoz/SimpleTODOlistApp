from fastapi import FastAPI
from app.routers import tasks

from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])