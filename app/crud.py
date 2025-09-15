from sqlalchemy.orm import Session
from app import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, status=task.status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task