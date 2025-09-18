from fastapi.encoders import jsonable_encoder

from app.routers.tasks import create_task
from app.schemas import TaskCreate
from app.models import StatusEnum

def test_create_task(client):
    task = TaskCreate(title = 'New task')

    response = client.post(
        '/tasks/',
        json=jsonable_encoder(task)
    )

    assert response is not None
    assert response.status_code == 201

    task_url = response.json()

    assert task_url['id'] is not None
    assert isinstance(task_url['id'], int)

    assert task_url['status'] is not None
    assert isinstance(StatusEnum(task_url['status']), StatusEnum)
    assert StatusEnum(task_url['status']) == StatusEnum.TODO

    assert task_url['title'] is not None
    assert (task_url['title'], str)
    assert task_url['title'] == task.title