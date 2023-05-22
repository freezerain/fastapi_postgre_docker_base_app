import json
import pytest

from app.DB import task_repository

test_task = {
    "id": 1,
    "title": "test task 1",
    "description": "",
    "end_date": "2023-05-21T20:27:19.262628",
    "created_by": "debug_python_code",
    "updated_by": "",
    "created_date": "2023-05-21T19:27:19.478860",
    "updated_date": "2023-05-21T19:27:19.478863"
}


def test_get_all_tasks(test_app, monkeypatch):
    test_response_payload = [test_task, test_task]

    async def mock_get_all():
        return test_response_payload

    monkeypatch.setattr(task_repository, "get_all", mock_get_all)

    response = test_app.get("/tasks")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_create(test_app, monkeypatch):
    test_request_payload = test_task

    async def mock_create(payload):
        return payload

    monkeypatch.setattr(task_repository, "create", mock_create)

    response = test_app.post("/tasks", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json() == test_request_payload


def test_create_validation_error(test_app):
    response = test_app.post("/tasks", content=json.dumps({"description": "mock_test_desc"}))
    assert response.status_code == 422


def test_get_task(test_app, monkeypatch):
    test_response_payload = test_task

    async def mock_get_by_id(temp_task_id):
        return test_response_payload

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)

    response = test_app.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_get_task_404_error(test_app, monkeypatch):
    async def mock_get_by_id(temp_task_id):
        return None

    # Maybe should test on real DB connection
    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    response = test_app.get("/tasks/-1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(test_app, monkeypatch):
    test_update_payload = test_task

    async def mock_get_by_id(temp_task_id):
        return test_update_payload

    async def mock_update(temp_task_id, task_data):
        return task_data

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    monkeypatch.setattr(task_repository, "update", mock_update)

    response = test_app.put("/tasks/1", content=json.dumps(test_update_payload))
    assert response.status_code == 200
    assert response.json() == test_update_payload


@pytest.mark.parametrize(
    "task_id, payload, status_code",
    [
        [-1, {"title": "2"}, 404],
        [1, {"id": "1"}, 422],
        [1, {}, 422]
    ]
)
def test_update_task_422_404_error(test_app, monkeypatch, task_id, payload, status_code):
    async def mock_get_by_id(temp_task_id):
        return True if temp_task_id == 1 else False

    async def mock_update(temp_task_id, task_data):
        return task_data

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    monkeypatch.setattr(task_repository, "update", mock_update)

    response = test_app.put(f"/tasks/{task_id}/", content=json.dumps(payload), )
    assert response.status_code == status_code


def test_delete_task_by_id(test_app, monkeypatch):
    test_task_response = test_task

    async def mock_get_by_id(temp_task_id):
        return test_task_response

    async def mock_delete(temp_task_id):
        return test_task_response

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    monkeypatch.setattr(task_repository, "delete", mock_delete)

    response = test_app.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json() == test_task_response


def test_delete_404_error(test_app, monkeypatch):
    async def mock_get_by_id(temp_task_id):
        return None

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)

    response = test_app.delete("/tasks/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
