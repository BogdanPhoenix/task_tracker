from datetime import datetime, timedelta

from src.models.task import Task, TaskStatus

mock_now = datetime.now()
mock_dict = {"id": 1, "description": "Test", "status": "todo", "createdAt": mock_now.isoformat(), "updatedAt": mock_now.isoformat()}

def test_correct_init():
    current = Task(1)
    expected = Task(id=1, description="", status=TaskStatus.TODO)

    assert current == expected
    assert current.created_at is not None
    assert current.updated_at is not None
    assert current.created_at == current.updated_at


def test_convert_to_dict():
    obj = Task(id=1, description="Test", status=TaskStatus.TODO, created_at=mock_now, updated_at=mock_now)
    current = obj.convert_to_dict()

    assert current == mock_dict


def test_convert_from_dict():
    expected = Task(id=1, description="Test", status=TaskStatus.TODO, created_at=mock_now, updated_at=mock_now)
    current = Task.convert_from_dict(mock_dict)

    assert current == expected
    assert current.created_at is not None
    assert current.updated_at is not None


def test_invalid_convert_from_dict():
    invalid_dict = {"id": 1, "description": "ok"}
    current = Task.convert_from_dict(invalid_dict)

    assert current is None


def test_change_description():
    mock_past = mock_now - timedelta(hours=1)
    new_description = "New text"
    expected = Task(id=1, description=new_description, status=TaskStatus.TODO, created_at=mock_past, updated_at=mock_past)

    obj = Task(id=1, description="Test", status=TaskStatus.TODO, created_at=mock_past, updated_at=mock_past)
    obj.change_description(new_description)

    assert obj == expected
    assert obj.created_at == expected.created_at
    assert mock_past < obj.updated_at


def test_change_status():
    mock_past = mock_now - timedelta(days=1)
    new_status = TaskStatus.IN_PROGRESS
    expected = Task(id=1, description="Test", status=new_status, created_at=mock_past, updated_at=mock_past)

    obj = Task(id=1, description="Test", status=TaskStatus.TODO, created_at=mock_past, updated_at=mock_past)
    obj.change_status(TaskStatus.IN_PROGRESS)

    assert obj == expected
    assert obj.created_at == expected.created_at
    assert mock_past < obj.updated_at


def test_empty_description():
    obj = Task(id=2, description="   ")
    assert obj.description == "   "


def test_special_characters_description():
    special_text = 'Task with "quotes", \\slashes\\ and emoji 🚀'
    obj = Task(id=3, description=special_text)
    
    as_dict = obj.convert_to_dict()
    assert as_dict["description"] == special_text
    
    restored = Task.convert_from_dict(as_dict)
    assert restored.description == special_text


def test_large_id():
    large_id = 999_999_999_999
    obj = Task(id=large_id)
    assert obj.id == large_id
    assert obj.convert_to_dict()["id"] == large_id


def test_id_as_string_in_init():
    obj = Task(id="123")
    assert obj.convert_to_dict()["id"] == "123"
