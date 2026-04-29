from functools import wraps

import pytest

from unittest.mock import patch

from src.models.task import Task, TaskStatus
from src.storage.json_storage import JsonTaskRepository
from src.services.task_service import TaskService

@pytest.fixture
def temp_storage(tmp_path):
    file_path = tmp_path / "tasks.json"
    return JsonTaskRepository(str(file_path))


@pytest.fixture
def temp_service(temp_storage):
    return TaskService(temp_storage)


def test_add_task_correctly(temp_service):
    description = "First Task"
    task = temp_service.add_task(description)

    assert task.id == 1
    assert task.description == description


def test_add_multiple_tasks_increments_id(temp_service):
    first_task = temp_service.add_task("First")
    second_task = temp_service.add_task("Second")

    assert first_task.id == 1
    assert second_task.id == 2


def test_add_task_calls_repository_save(temp_storage, temp_service):
    with patch.object(temp_storage, 'add', wraps=temp_storage.add) as mock_save:
        temp_service.add_task("Test")

        assert mock_save.called

        saved_task = mock_save.call_args[0][0]
        assert saved_task.description == "Test"


def test_add_task_handles_storage_failure(temp_storage):
    service = TaskService(temp_storage)

    with patch.object(temp_storage, 'add', side_effect=Exception("Disk error")):
        with pytest.raises(Exception, match="Disk error"):
            service.add_task("Will fail")


def test_add_task_with_very_long_description(temp_service):
    long_desc = "A" * 1000
    task = temp_service.add_task(long_desc)

    assert task.description == long_desc


def test_delete_task_correctly(temp_storage, temp_service):
    temp_service.add_task("First Task")
    temp_service.add_task("Second Task")

    task = temp_service.delete_task(id=1)
    tasks = temp_storage.get_all()

    assert len(tasks) == 1
    assert tasks[0].id == 2
    assert task.id == 1


def test_delete_task_raises_error_if_not_found(temp_service):
    with pytest.raises(ValueError, match="Task with id = 99 not found"):
        temp_service.delete_task(id=99)


def test_delete_only_task_clears_storage(temp_service, temp_storage):
    temp_service.add_task("The only one")
    temp_service.delete_task(id=1)
    assert temp_storage.get_all() == []


def test_delete_sequential_tasks(temp_service, temp_storage):
    service = temp_service
    service.add_task("T1")
    service.add_task("T2")
    service.add_task("T3")

    service.delete_task(id=1)
    service.delete_task(id=3)

    remaining = temp_storage.get_all()
    assert len(remaining) == 1
    assert remaining[0].description == "T2"


def test_get_all_correctly(temp_service):
    temp_service.add_task("First")
    temp_service.add_task("Second")

    tasks = temp_service.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[1].description == "Second"
    assert tasks[0].description == "First"


def test_get_all_from_empty_storage(temp_service):
    tasks = temp_service.get_all_tasks()
    assert len(tasks) == 0


def test_get_all_calls_repository_get_all(temp_storage, temp_service):
    with patch.object(temp_storage, 'get_all', wraps=temp_storage.get_all) as mock_get_all:
        temp_service.add_task("First")
        temp_service.add_task("Second")

        tasks = temp_service.get_all_tasks()
        assert mock_get_all.called

        assert isinstance(tasks, list)
        assert len(tasks) == 2
        assert tasks[0].id == 1


def test_get_task_by_id_correctly(temp_service):
    original_task = temp_service.add_task("Initial")
    current_task = temp_service.get_task_by_id(original_task.id)

    assert current_task == original_task


def test_get_task_by_id_raise_error_if_not_found(temp_service):
    with pytest.raises(ValueError, match="Task with id = 999 not found"):
        temp_service.get_task_by_id(999)


def test_update_task_description_correctly(temp_service):
    original_task = temp_service.add_task("Initial")
    task_id = original_task.id

    updated_task = temp_service.update_task_description(task_id, "Updated")

    assert updated_task.description == "Updated"
    assert updated_task.id == task_id
    assert updated_task.updated_at > original_task.created_at


def test_update_task_description_raises_error_if_not_found(temp_service):
    with pytest.raises(ValueError, match="Task with id = 999 not found"):
        temp_service.update_task_description(999, "New Description")


def test_update_task_description_raises_error_if_empty(temp_service):
    task = temp_service.add_task("Initial")

    with pytest.raises(ValueError, match="Description cannot be empty"):
        temp_service.update_task_description(task.id, "   ")


def test_update_task_status_correctly(temp_service):
    original_task = temp_service.add_task("Initial")
    task_id = original_task.id

    updated_task = temp_service.update_task_status(task_id, TaskStatus.IN_PROGRESS)

    assert updated_task.status == TaskStatus.IN_PROGRESS
    assert updated_task.id == task_id
    assert updated_task.updated_at > original_task.created_at


def test_update_task_status_raises_error_if_not_found(temp_service):
    with pytest.raises(ValueError, match="Task with id = 999 not found"):
        temp_service.update_task_status(999, TaskStatus.DONE)


def test_update_task_status_raises_error_on_invalid_type(temp_service):
    task = temp_service.add_task("Initial")

    with pytest.raises(Exception):
        temp_service.update_task_status(task.id, "invalid_status_string")
