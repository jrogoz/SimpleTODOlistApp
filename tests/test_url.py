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

def create_multiple_tasks(client, num=2):
    tasks_response = []
    for _ in range(num):
        _, response = create_simple_task(client)
        tasks_response.append(response)
    return tasks_response

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

def test_get_all_tasks(client):
    response = create_multiple_tasks(client)
    tasks = [res.json() for res in response]

    response = client.get('/tasks/')

    assert response is not None
    assert response.status_code == 200

    all_tasks_url = response.json()

    assert isinstance(all_tasks_url, list)
    assert len(all_tasks_url) == len(tasks)

    for t, t_url in zip(tasks, all_tasks_url):

        assert t['id'] == t_url['id']
        assert t['status'] == t_url['status']
        assert t['title'] == t_url['title']

def test_get_all_tasks_no_tasks(client):
    response = client.get('/tasks/')

    assert response is not None
    assert response.status_code == 200

    assert response.json() == []