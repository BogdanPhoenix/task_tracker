import os
import pytest
from unittest.mock import patch
from src.models.task import Task, TaskStatus
from src.storage.json_storage import JsonTaskRepository


@pytest.fixture
def temp_storage(tmp_path):
    file_path = tmp_path / "tasks.json"
    return JsonTaskRepository(str(file_path))


def test_add_task_to_empty_storage(temp_storage):
    new_task = Task(id=0, description="First")
    saved_task = temp_storage.add(new_task)

    assert saved_task.id == 1
    assert len(temp_storage.get_all()) == 1


def test_add_task_increments_id_correctly(temp_storage):
    temp_storage.add(Task(id=0, description="Task 1"))
    second_task = temp_storage.add(Task(id=0, description="Task 2"))

    assert second_task.id == 2
    assert temp_storage.get_all()[1].description == "Task 2"


def test_add_task_persists_data(temp_storage):
    from datetime import datetime
    task = Task(id=0, description="Persistent Task")
    temp_storage.add(task)

    loaded_tasks = temp_storage.get_all()
    assert loaded_tasks[0].description == "Persistent Task"
    assert isinstance(loaded_tasks[0].created_at, datetime)


def test_get_all_returns_empty_list_when_file_not_found(temp_storage):
    assert temp_storage.get_all() == []


def test_save_and_get_all_integration(temp_storage):
    tasks = [Task(id=1, description="Test task")]
    temp_storage.save_all(tasks)

    loaded_tasks = temp_storage.get_all()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].id == 1
    assert loaded_tasks[0].description == "Test task"


def test_get_by_id_success(temp_storage):
    tasks = [Task(id=1, description="Target"), Task(id=2, description="Other")]
    temp_storage.save_all(tasks)

    task = temp_storage.get_by_id(1)
    assert task.description == "Target"


def test_get_by_id_not_found_raises_error(temp_storage):
    temp_storage.save_all([])
    with pytest.raises(ValueError, match="Task with id = 99 not found"):
        temp_storage.get_by_id(99)


def test_atomic_save_failure_cleanup(temp_storage):
    tasks = [Task(id=1)]

    with patch("os.replace", side_effect=OSError("Disk full")):
        with pytest.raises(Exception, match="Failed to save data"):
            temp_storage.save_all(tasks)

    assert not os.path.exists(temp_storage.temp_file_path)


def test_save_all_preserves_task_object_identity(temp_storage):
    original_task = Task(id=1, description="Test")
    tasks = [original_task]

    temp_storage.save_all(tasks)

    loaded = temp_storage.get_by_id(1)
    assert loaded == original_task


def test_read_raw_data_ignores_invalid_json(temp_storage):
    with open(temp_storage.file_path, "w") as f:
        f.write("[\"oops\"]")

    assert temp_storage._read_raw_data() == []


def test_get_all_skips_invalid_task_records(temp_storage):
    with open(temp_storage.file_path, "w") as f:
        f.write('[{"id": 1, "description": "ok"}, {"id": "bad"}]')

    tasks = temp_storage.get_all()
    assert len(tasks) == 0


def test_delete_by_id_success(temp_storage):
    tasks = [
        Task(id=1, description="First"),
        Task(id=2, description="Second"),
        Task(id=3, description="Third")
    ]
    temp_storage.save_all(tasks)

    removed_task = temp_storage.delete_by_id(2)

    assert removed_task.id == 2
    assert removed_task.description == "Second"

    remaining_tasks = temp_storage.get_all()
    assert len(remaining_tasks) == 2
    assert all(t.id != 2 for t in remaining_tasks)


def test_delete_by_id_raises_value_error_if_not_found(temp_storage):
    temp_storage.save_all([Task(id=1, description="Test")])

    with pytest.raises(ValueError, match="Task with id = 999 not found"):
        temp_storage.delete_by_id(999)


def test_delete_by_id_with_empty_storage(temp_storage):
    with pytest.raises(ValueError, match="Task with id = 1 not found"):
        temp_storage.delete_by_id(1)


def test_delete_all_removes_all_tasks(temp_storage):
    tasks = [Task(id=1, description="Task 1"), Task(id=2, description="Task 2")]
    temp_storage.save_all(tasks)
    assert len(temp_storage.get_all()) == 2

    temp_storage.delete_all()
    assert temp_storage.get_all() == []


def test_delete_all_works_if_file_not_exists(temp_storage):
    temp_storage.delete_all()
    assert temp_storage.get_all() == []


def test_delete_all_raises_exception_on_failure(temp_storage):
    with patch.object(temp_storage, '_save_json', side_effect=Exception("System failure")):
        with pytest.raises(Exception, match="Unable to delete the contents of the file"):
            temp_storage.delete_all()


def test_update_correctly(temp_storage):
    expected = Task(id=1, description="Test", status=TaskStatus.IN_PROGRESS)
    new_task = Task(id=1, description="Test", status=TaskStatus.IN_PROGRESS)

    temp_storage.add(Task(description="Test"))
    updated = temp_storage.update(new_task)

    assert updated == expected


def test_update_raises_error_if_id_not_found(temp_storage):
    new_task = Task(id=999, description="Test Update", status=TaskStatus.DONE)

    with pytest.raises(ValueError, match="Task with id = 999 not found"):
        temp_storage.update(new_task)


def test_update_preserves_other_fields(temp_storage):
    task = temp_storage.add(Task(description="Initial"))
    original_created_at = task.created_at

    task.description = "Updated"
    updated = temp_storage.update(task)

    assert updated.description == "Updated"
    assert updated.status == TaskStatus.TODO
    assert updated.created_at == original_created_at


def test_update_atomic_failure_protection(temp_storage):
    task = temp_storage.add(Task(description="Safe"))
    task.description = "Danger"

    with patch("os.replace", side_effect=OSError("Disk Full")):
        with pytest.raises(Exception, match="Failed to save data"):
            temp_storage.update(task)

    assert temp_storage.get_by_id(task.id).description == "Safe"
