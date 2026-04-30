#!/usr/bin/env python

import os.path
from argparse import Namespace

from src.cli.parser import parser_args
from src.models.task import TaskStatus, Task
from src.storage.json_storage import JsonTaskRepository
from src.services.task_service import TaskService
from src.utils.printer import Printer


def handle_add(service: TaskService, args: Namespace) -> None:
    task = service.add_task(args.description)
    Printer.success("Task added", task)


def handle_update(service: TaskService, args: Namespace) -> None:
    task = service.update_task_description(args.id, args.description)
    Printer.success("Task description updated", task)


def handle_delete(service: TaskService, args: Namespace) -> None:
    task = service.delete_task(args.id)
    Printer.success("Task deleted", task)


def handle_mark(service: TaskService, args: Namespace) -> None:
    status = TaskStatus(args.status)
    task = service.update_task_status(args.id, status)
    Printer.success("Task status updated", task)


def handle_list(service: TaskService, args: Namespace) -> None:
    if args.status:
        status = TaskStatus(args.status)
        tasks = service.get_tasks_by_status(status)
    else:
        tasks = service.get_all_tasks()

    Printer.task_list(tasks)


def error_handler(func):
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
