import pytest
from argparse import Namespace
from unittest.mock import MagicMock, patch, ANY

import src.main as main
from src.models.task import Task, TaskStatus


@patch("src.main.Printer.success")
def test_handle_add_calls_printer_with_correct_object(mock_success):
    mock_service = MagicMock()
    returned_task = Task(id=1, description="Test")
    mock_service.add_task.return_value = returned_task

    args = Namespace(description="Test")

    main.handle_add(mock_service, args)
    mock_success.assert_called_once_with(ANY, returned_task)


@patch("src.main.Printer.success")
def test_handle_update_calls_printer_with_correct_object(mock_success):
    mock_service = MagicMock()
    returned_task = Task(id=1, description="Test")
    mock_service.update_task_description.return_value = returned_task

    args = Namespace(id=1, description="Test")

    main.handle_update(mock_service, args)
    mock_success.assert_called_once_with(ANY, returned_task)


@patch("src.main.Printer.success")
def test_handle_delete_calls_printer_with_correct_object(mock_success):
    mock_service = MagicMock()
    returned_task = Task(id=1, description="Test")
    mock_service.delete_task.return_value = returned_task

    args = Namespace(id=1)

    main.handle_delete(mock_service, args)
    mock_success.assert_called_once_with(ANY, returned_task)


@patch("src.main.Printer.success")
def test_handle_mark_calls_printer_with_correct_object(mock_success):
    mock_service = MagicMock()
    returned_task = Task(id=1, description="Test", status=TaskStatus.IN_PROGRESS)
    mock_service.update_task_status.return_value = returned_task

    args = Namespace(id=1, status="in-progress")

    main.handle_mark(mock_service, args)
    mock_success.assert_called_once_with(ANY, returned_task)


@patch("src.main.Printer.task_list")
def test_handle_list_calls_printer_with_correct_object(mock_task_list):
    mock_service = MagicMock()
    returned_task = [Task(id=1, description="Test")]
    mock_service.get_all_tasks.return_value = returned_task

    args = Namespace(status=None)

    main.handle_list(mock_service, args)
    mock_task_list.assert_called_once_with(returned_task)


@patch("src.main.Printer.error")
def test_error_handler_handles_value_error(mock_error):
    @main.error_handler
    def failing_func():
        raise ValueError("Business error")

    failing_func()
    mock_error.assert_called_once_with("Business error")


@patch("src.main.Printer.critical")
def test_error_handler_handles_unexpected_error(mock_critical):
    @main.error_handler
    def crashing_func():
        raise Exception("System crash")

    crashing_func()
    mock_critical.assert_called_once_with("System crash")


def test_handle_add_propagates_value_error():
    mock_service = MagicMock()
    mock_service.add_task.side_effect = ValueError("Description empty")
    args = Namespace(description=" ")

    with pytest.raises(ValueError, match="Description empty"):
        main.handle_add(mock_service, args)


def test_handle_update_propagates_value_error():
    mock_service = MagicMock()
    mock_service.update_task_description.side_effect = ValueError("Not found")
    args = Namespace(id=999, description="New")

    with pytest.raises(ValueError, match="Not found"):
        main.handle_update(mock_service, args)


def test_handle_delete_propagates_value_error():
    mock_service = MagicMock()
    mock_service.delete_task.side_effect = ValueError("ID not exists")
    args = Namespace(id=999)

    with pytest.raises(ValueError, match="ID not exists"):
        main.handle_delete(mock_service, args)


def test_handle_mark_propagates_value_error():
    mock_service = MagicMock()
    mock_service.update_task_status.side_effect = ValueError("Invalid status change")
    args = Namespace(id=1, status="done")

    with pytest.raises(ValueError, match="Invalid status change"):
        main.handle_mark(mock_service, args)
