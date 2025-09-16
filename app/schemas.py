from pydantic import BaseModel
from typing import Optional
from app.models import StatusEnum

class TaskCreate(BaseModel):
    title: str
    status: Optional[StatusEnum] = StatusEnum.TODO

class TaskRead(BaseModel):
    id: int
    title: str
    status: StatusEnum

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[StatusEnum] = None
