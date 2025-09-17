
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

def test_get_all_tasks(db_session):

    tasks = [
        create_simple_task(db_session),
        create_simple_task(db_session)
    ]
    

    all_tasks_db = crud.get_tasks(db=db_session)

    assert isinstance(all_tasks_db, list)
    assert len(all_tasks_db) == 2

    for t, t_db in zip(tasks, all_tasks_db):
        assert isinstance(t_db, object)

        assert t.id == t_db.id
        assert t.title == t_db.title
        assert t.status == t_db.status

def test_get_all_tasks_no_tasks(db_session):
    all_tasks_db = crud.get_tasks(db=db_session)

    assert all_tasks_db is not None
    assert all_tasks_db == []

