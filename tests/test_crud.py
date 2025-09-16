
from app import crud
from app.schemas import TaskCreate, TaskRead
from app.models import StatusEnum

def test_create_task(db_session):
    task = TaskCreate(title="Some title")
    task_db = crud.create_task(db=db_session, task=task)

    assert task_db is not None
    assert isinstance(task_db, object)

    assert task_db.id is not None
    assert isinstance(task_db.id, int)

    assert task_db.title == task.title

    assert task_db.status is not None
    assert task_db.status == StatusEnum.TODO