import argparse

from src.models.task import TaskStatus


def build_parser() -> argparse.ArgumentParser:
    list_status = [status.value for status in TaskStatus]
    mark_status = [value for value in list_status if value != TaskStatus.TODO.value]

    parser = argparse.ArgumentParser(prog="task-cli")
    subparser = parser.add_subparsers(dest="command", required=True)

    add_parser = subparser.add_parser("add")
    add_parser.add_argument("description", type=str, help="Description of the task")
    add_parser.set_defaults(func="add")

    update_parser = subparser.add_parser("update")
    update_parser.add_argument("id", type=int, help="ID of the task to update")
    update_parser.add_argument("description", type=str, help="New description of the task")
    update_parser.set_defaults(func="update")

    delete_parser = subparser.add_parser("delete")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")
    delete_parser.set_defaults(func="delete")

    mark_parser = subparser.add_parser("mark")
    mark_parser.add_argument("id", type=int, help="ID of the task to change status")
    mark_parser.add_argument("status", type=str, choices=mark_status, help="New status of the task")
    mark_parser.set_defaults(func="mark")

    list_parser = subparser.add_parser("list")
    list_parser.add_argument("status", nargs='?', choices=list_status, help="Status of the task to list")
    list_parser.set_defaults(func="list")

    return parser


def parser_args():
    parser = build_parser()
    return parser.parse_args()