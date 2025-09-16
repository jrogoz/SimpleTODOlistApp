
from app import crud
from app.schemas import TaskCreate, TaskRead
from app.models import StatusEnum

def create_simple_task(db_session):
    task = TaskCreate(title="Some title")
    return crud.create_task(db=db_session, task=task)

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

def test_get_task(db_session):
    task = create_simple_task(db_session)
    task_db = crud.get_task(db=db_session, task_id=task.id)

    assert task_db is not None
    assert isinstance(task_db, object)

    assert task_db.id == task.id
    assert task_db.status == task.status
    assert task_db.title == task.title


def test_get_task_invalid_task_id(db_session):
    task_db = crud.get_task(db=db_session, task_id=1234)

    assert task_db is None
