# Task Tracker CLI

You can view the problem statement at the following [link](https://roadmap.sh/projects/task-tracker).

A robust, modular, and professional Command-Line Interface (CLI) application for tracking tasks. Built with Python using a clean architecture (Service/Repository pattern) and atomic JSON persistence.

## Features

- **Task Management**: Add, update, delete, and list tasks effortlessly.
- **Status Tracking**: Transition tasks through `todo`, `in-progress`, and `done` states.
- **Atomic Persistence**: Data is saved securely in a JSON file with atomic write operations to prevent data loss.
- **Professional UI**: Clean console output with emojis, structured tables, and clear status formatting.
- **Robust Error Handling**: Centralized exception handling ensures the application never crashes and provides helpful feedback.
- **Highly Testable**: Comprehensive test suite covering models, services, and CLI orchestration.

## Installation

To install the application and enable the `task-cli` command globally in your environment, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd task_tracker
   ```

2. **(Recommended) Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install in editable mode**:
   This step registers the `task-cli` command so you can run it from anywhere.
   ```bash
   pip install -e .
   ```

## Usage

Once installed, use the `task-cli` command followed by a subcommand:

### Add a new task
```bash
task-cli add "Buy groceries"
```

### Update a task
```bash
task-cli update 1 "Buy groceries and cook dinner"
```

### Delete a task
```bash
task-cli delete 1
```

### Change task status
```bash
task-cli mark 1 in-progress
task-cli mark 1 done
```

### List tasks
- **All tasks**:
  ```bash
  task-cli list
  ```
- **Filter by status**:
  ```bash
  task-cli list todo
  task-cli list in-progress
  task-cli list done
  ```

## Running Tests

The project uses `pytest` for testing. To run the full test suite:

```bash
pytest
```

## Project Structure

- `src/main.py`: Application entry point and command orchestration.
- `src/cli/parser.py`: CLI argument parsing logic.
- `src/services/task_service.py`: Core business logic.
- `src/models/task.py`: Data models and Enums.
- `src/storage/`: Data persistence layer (JSON).
- `src/utils/printer.py`: Console output formatting.
- `tests/`: Comprehensive unit and integration tests.
