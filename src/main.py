#!/usr/bin/env python

import os.path
from argparse import Namespace

from src.cli.parser import parser_args
from src.models.task import TaskStatus, Task
from src.storage.json_storage import JsonTaskRepository
from src.services.task_service import TaskService
from src.utils.printer import Printer


def handle_add(service: TaskService, args: Namespace) -> None:
    """
    Handles the addition of a new task via the CLI.

    Args:
        service (TaskService): The task management service.
        args (Namespace): CLI arguments containing the task description.
    """

    task = service.add_task(args.description)
    Printer.success("Task added", task)


def handle_update(service: TaskService, args: Namespace) -> None:
    """
    Handles the modification of an existing task's description.

    Args:
        service (TaskService): The task management service.
        args (Namespace): CLI arguments containing the task ID and new description.
    """

    task = service.update_task_description(args.id, args.description)
    Printer.success("Task description updated", task)


def handle_delete(service: TaskService, args: Namespace) -> None:
    """
    Handles the deletion of a task.

    Args:
        service (TaskService): The task management service.
        args (Namespace): CLI arguments containing the ID of the task to be removed.
    """

    task = service.delete_task(args.id)
    Printer.success("Task deleted", task)


def handle_mark(service: TaskService, args: Namespace) -> None:
    """
    Handles the status transition of a task.

    Args:
        service (TaskService): The task management service.
        args (Namespace): CLI arguments containing the task ID and the target status.
    """

    status = TaskStatus(args.status)
    task = service.update_task_status(args.id, status)
    Printer.success("Task status updated", task)


def handle_list(service: TaskService, args: Namespace) -> None:
    """
    Handles the retrieval and display of tasks, optionally filtered by status.

    Args:
        service (TaskService): The task management service.
        args (Namespace): CLI arguments containing the optional status filter.
    """

    if args.status:
        status = TaskStatus(args.status)
        tasks = service.get_tasks_by_status(status)
    else:
        tasks = service.get_all_tasks()

    Printer.task_list(tasks)


def error_handler(func):
    """
    Decorator for centralized exception handling across command handlers.

    This decorator captures ValueErrors (business logic violations) and 
    general Exceptions, redirecting them to the Printer's error or critical methods.

    Args:
        func (Callable): The function to be wrapped with error handling logic.

    Returns:
        Callable: The wrapped function.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            Printer.error(str(e))
        except Exception as e:
            Printer.critical(str(e))
    return wrapper


COMMAND_HANDLERS = {
        "add": handle_add,
        "update": handle_update,
        "delete": handle_delete,
        "mark": handle_mark,
        "list": handle_list
    }


@error_handler
def main():
    """
    Main entry point for the Task Tracker CLI application.

    Initializes the infrastructure (storage, service, parser) and dispatches 
    control to the appropriate command handler based on user input.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", "tasks.json")

    repository = JsonTaskRepository(file_path)
    service = TaskService(repository)
    args = parser_args()

    handle = COMMAND_HANDLERS.get(args.func)

    if handle:
        handle(service, args)


if __name__ == "__main__":
    main()
