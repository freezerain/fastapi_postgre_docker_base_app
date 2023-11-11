"""
Test Task API
"""

import json
import pytest

from app.DB import task_repository

# Sample task data for testing
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


def test_get_all_tasks(postgres_client, monkeypatch):
    """
    Test get all tasks.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "get_all" call.
    :return: None
    """
    test_response_payload = [test_task, test_task]

    async def mock_get_all():
        return test_response_payload

    monkeypatch.setattr(task_repository, "get_all", mock_get_all)

    response = postgres_client.get("/tasks")

    # Assertion
    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_create(postgres_client, monkeypatch):
    """
    Test creating a task.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "create" call.
    :return: None
    """
    test_request_payload = test_task

    async def mock_create(payload):
        return payload

    monkeypatch.setattr(task_repository, "create", mock_create)

    response = postgres_client.post("/tasks", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json() == test_request_payload


def test_create_validation_error(postgres_client):
    """
    Test validation error during task creation.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :return: None
    """
    response = postgres_client.post("/tasks", content=json.dumps({"description": "mock_test_desc"}))

    assert response.status_code == 422


def test_get_task(postgres_client, monkeypatch):
    """
    Test retrieving a specific task.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "get_by_id" call.
    :return: None
    """
    test_response_payload = test_task

    async def mock_get_by_id(temp_task_id):
        return test_response_payload

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)

    response = postgres_client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_get_task_404_error(postgres_client, monkeypatch):
    """
    Test 404 error when retrieving a non-existing task.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "get_by_id" call.
    :return: None
    """

    async def mock_get_by_id(temp_task_id):
        return None

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    response = postgres_client.get("/tasks/-1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(postgres_client, monkeypatch):
    """
    Test updating a task.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "get_by_id" and "update" calls.
    :return: None
    """
    test_update_payload = test_task

    async def mock_get_by_id(temp_task_id):
        return test_update_payload

    async def mock_update(temp_task_id, task_data):
        return task_data

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    monkeypatch.setattr(task_repository, "update", mock_update)

    response = postgres_client.put("/tasks/1", content=json.dumps(test_update_payload))

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
def test_update_task_422_404_error(postgres_client, monkeypatch, task_id, payload, status_code):
    """
    Test 422 and 404 errors during task update.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "get_by_id" and "update" calls.
    :param task_id: Task ID for testing different scenarios.
    :param payload: Payload for testing different scenarios.
    :param status_code: Expected HTTP status code.
    :return: None
    """

    async def mock_get_by_id(temp_task_id):
        return True if temp_task_id == 1 else False

    async def mock_update(temp_task_id, task_data):
        return task_data

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    monkeypatch.setattr(task_repository, "update", mock_update)

    response = postgres_client.put(f"/tasks/{task_id}/", content=json.dumps(payload), )

    assert response.status_code == status_code


def test_delete_task_by_id(postgres_client, monkeypatch):
    """
    Test deleting a task by ID.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "get_by_id" and "delete" calls.
    :return: None
    """
    test_task_response = test_task

    async def mock_get_by_id(temp_task_id):
        return test_task_response

    async def mock_delete(temp_task_id):
        return test_task_response

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)
    monkeypatch.setattr(task_repository, "delete", mock_delete)

    response = postgres_client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json() == test_task_response


def test_delete_404_error(postgres_client, monkeypatch):
    """
    Test 404 error when deleting a non-existing task.
    :param postgres_client: A client for making requests to the PostgreSQL database.
    :param monkeypatch: Used for mocking the "get_by_id" call.
    :return: None
    """

    async def mock_get_by_id(temp_task_id):
        return None

    monkeypatch.setattr(task_repository, "get_by_id", mock_get_by_id)

    response = postgres_client.delete("/tasks/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
