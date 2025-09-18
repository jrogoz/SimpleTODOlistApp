from fastapi.encoders import jsonable_encoder

from app.routers.tasks import create_task
from app.schemas import TaskCreate
from app.models import StatusEnum

def create_simple_task(client):
    task = TaskCreate(title = 'New task')
    response = client.post(
        '/tasks/',
        json=jsonable_encoder(task)
    )
    return task, response

def test_create_task(client):
    task, response = create_simple_task(client)

    assert response is not None
    assert response.status_code == 201

    task_url = response.json()

    assert task_url['id'] is not None
    assert isinstance(task_url['id'], int)

    assert task_url['status'] is not None
    assert isinstance(StatusEnum(task_url['status']), StatusEnum)
    assert StatusEnum(task_url['status']) == StatusEnum.TODO

    assert task_url['title'] is not None
    assert isinstance(task_url['title'], str)
    assert task_url['title'] == task.title

def test_get_task(client):
    _, response = create_simple_task(client)

    task = response.json()

    response = client.get(f'/tasks/{task['id']}')

    assert response is not None
    assert response.status_code == 200

    task_url = response.json()

    assert task_url['id'] is not None
    assert isinstance(task_url['id'], int)
    assert task_url['id'] == task_url['id']

    assert task_url['title'] is not None
    assert isinstance(task_url['title'], str)
    assert task_url['title'] == task_url['title']

    assert task_url['status'] is not None
    assert isinstance(StatusEnum(task_url['status']), StatusEnum)
    assert task_url['status'] == task_url['status']

def test_get_task_invalid_id(client):
    response = client.get('/tasks/12345')

    assert response is not None
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}