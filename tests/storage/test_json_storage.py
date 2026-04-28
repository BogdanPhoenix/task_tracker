import os
import pytest
from unittest.mock import patch
from src.models.task import Task
from src.storage.json_storage import JsonTaskRepository


@pytest.fixture
def temp_storage(tmp_path):
    file_path = tmp_path / "tasks.json"
    return JsonTaskRepository(str(file_path))


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

