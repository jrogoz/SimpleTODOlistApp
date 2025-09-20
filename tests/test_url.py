from fastapi.encoders import jsonable_encoder

from app.routers.tasks import create_task
from app.schemas import TaskCreate, TaskUpdate
from app.models import StatusEnum

def create_simple_task(client):
    task = TaskCreate(title = 'New task')
    response = client.post(
        '/tasks/',
        json=jsonable_encoder(task)
    )
    return task, response

def create_multiple_tasks(client, num:int = 2):
    tasks_response = []
    for _ in range(num):
        _, response = create_simple_task(client)
        tasks_response.append(response)
    return tasks_response

def update_task(client, task_id, update_data:dict):
    task_update = TaskUpdate(**update_data)
    response = client.put(
        f'/tasks/{task_id}',
        json=jsonable_encoder(task_update)
    )
    return task_update, response

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
    assert task_url['id'] == task['id']

    assert task_url['title'] is not None
    assert isinstance(task_url['title'], str)
    assert task_url['title'] == task['title']

    assert task_url['status'] is not None
    assert isinstance(StatusEnum(task_url['status']), StatusEnum)
    assert task_url['status'] == task['status']

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


def test_update_task(client):
    _, response = create_simple_task(client)
    task = response.json()
    update_data = {'title':'New title', 'status':'done'}
    task_update, response = update_task(client, task['id'], update_data)

    assert response is not None
    assert response.status_code == 200

    task_url = response.json()
    assert isinstance(task_url, object)

    assert task_url['id'] is not None
    assert isinstance(task_url['id'], int)
    assert task_url['id'] == task['id']

    assert task_url['title'] is not None
    assert isinstance(task_url['title'], str)
    assert task_url['title'] != task['title']
    assert task_url['title'] == task_update.title

    assert task_url['status'] is not None
    assert task_url['status'] != task['status']
    assert task_url['status'] == task_update.status.value

def test_update_task_title_only(client):
    _, response = create_simple_task(client)
    task = response.json()
    update_data = {'title':'New title'}
    task_update, response = update_task(client, task['id'], update_data)

    assert response is not None
    assert response.status_code == 200

    task_url = response.json()
    assert isinstance(task_url, object)

    assert task_url['id'] is not None
    assert isinstance(task_url['id'], int)
    assert task_url['id'] == task['id']

    assert task_url['title'] is not None
    assert isinstance(task_url['title'], str)
    assert task_url['title'] != task['title']
    assert task_url['title'] == task_update.title

    assert task_url['status'] is not None
    assert task_url['status'] == task['status']


def test_update_task_status_only(client):
    _, response = create_simple_task(client)
    task = response.json()
    update_data = {'status':'in_progress'}
    task_update, response = update_task(client, task['id'], update_data)

    assert response is not None
    assert response.status_code == 200

    task_url = response.json()
    assert isinstance(task_url, object)

    assert task_url['id'] is not None
    assert isinstance(task_url['id'], int)
    assert task_url['id'] == task['id']

    assert task_url['title'] is not None
    assert isinstance(task_url['title'], str)
    assert task_url['title'] == task['title']

    assert task_url['status'] is not None
    assert task_url['status'] != task['status']
    assert task_url['status'] == task_update.status.value

def test_update_task_invalid_id(client):
    update_data = {'title': 'New title', 'status': 'done'}
    _, response = update_task(client, task_id=1234, update_data=update_data)

    assert response is not None
    assert isinstance(response, object)
    assert response.status_code == 404

    assert response.json() == {'detail': 'Task not found'}

def test_delete_task(client):
    _, response = create_simple_task(client)
    task_id = response.json()['id']

    response = client.get(f'/tasks/')
    task_list_before = response.json()
    
    assert len(task_list_before) == 1

    response = client.delete(f'/tasks/{task_id}')

    assert response is not None
    assert response.status_code == 204

    response = client.get(f'/tasks/')
    task_list_before = response.json()
    
    assert len(task_list_before) == 0

def test_delete_task_invalid_id(client):
    response = client.delete(f'/tasks/1234')

    assert response is not None
    assert response.status_code == 404

    assert response.json() == {'detail': 'Task not found'}