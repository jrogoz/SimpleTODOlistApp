from sqlalchemy.orm import Session
from app import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, status=task.status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(models.Task).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id==task_id).first()

def update_task(db: Session, task_id: int, new_task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if db_task:
        for key, value in new_task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)

        db.commit()
        db.refresh(db_task)
        return db_task
    return None
    

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False