import pytest

from src.cli.parser import build_parser


def test_add_parser():
    parser = build_parser()
    args = parser.parse_args(["add", "description"])

    assert args.command == "add"
    assert args.func == "add"
    assert args.description == "description"


def test_update_parser():
    parser = build_parser()
    args = parser.parse_args(["update", "1", "new description"])

    assert args.command == "update"
    assert args.func == "update"
    assert args.id == 1
    assert args.description == "new description"


def test_delete_parser():
    parser = build_parser()
    args = parser.parse_args(["delete", "1"])

    assert args.command == "delete"
    assert args.func == "delete"
    assert args.id == 1


def test_mark_parser():
    parser = build_parser()
    args = parser.parse_args(["mark", "1", "in-progress"])

    assert args.command == "mark"
    assert args.func == "mark"
    assert args.id == 1
    assert args.status == "in-progress"


def test_list_parser():
    parser = build_parser()
    args = parser.parse_args(["list"])

    assert args.command == "list"
    assert args.func == "list"
    assert args.status is None


def test_list_with_status_parser():
    parser = build_parser()
    args = parser.parse_args(["list", "in-progress"])

    assert args.command == "list"
    assert args.func == "list"
    assert args.status == "in-progress"


def test_parser_args_exception():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add"])


def test_mark_invalid_status_parser_exception():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["mark", "1", "invalid"])


def test_list_invalid_status_parser_exception():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["list", "invalid"])


def test_update_invalid_id_parser_exception():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["update", "invalid", "new description"])


def test_delete_invalid_id_parser_exception():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["delete", "invalid"])


def test_mark_invalid_id_parser_exception():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["mark", "invalid", "in-progress"])


def test_all_commands_combined_parser_exception():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add", "description", "update", "1", "new description", "delete", "1", "mark", "1", "in-progress", "list", "in-progress"])
        