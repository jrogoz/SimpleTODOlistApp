from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models import StatusEnum

class TaskCreate(BaseModel):
    title: str
    status: Optional[StatusEnum] = StatusEnum.TODO

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: StatusEnum

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[StatusEnum] = None
