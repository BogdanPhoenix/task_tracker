from src.models.task import Task

class Printer:
    """
    Utility class for handling command-line interface (CLI) output formatting.

    This class provides standardized methods for displaying success messages, 
    errors, and formatted lists of tasks to the user, ensuring a consistent 
    look and feel across the application.
    """

    @staticmethod
    def _format_task(task: Task) -> str:
        """
        Formats a single task object into a structured string for display.

        Args:
            task (Task): The task instance to format.

        Returns:
            str: A formatted string containing the task ID, status, and description.
        """

        return f"#{task.id:<3} | [{task.status_formatted:^11}] | {task.description}"

    @staticmethod
    def success(message: str, task: Task = None) -> None:
        """
        Displays a success message and optionally the details of a task.

        Args:
            message (str): The success message to be displayed.
            task (Task, optional): An associated task object to be printed below the message.
        """

        print(f"✅ {message}")
        if task:
            print(Printer._format_task(task))

    @staticmethod
    def error(message: str) -> None:
        """
        Displays an error message to the user.

        Args:
            message (str): The error message describing a non-critical issue.
        """

        print(f"❌ Error: {message}")

    @staticmethod
    def critical(message: str) -> None:
        """
        Displays a critical error message for unexpected system failures.

        Args:
            message (str): The message describing the critical failure.
        """

        print(f"💥 Critical Error: {message}")

    @staticmethod
    def task_list(tasks: list[Task]) -> None:
        """
        Displays a formatted table of multiple task entities.

        If the provided list is empty, a notification message is shown instead.

        Args:
            tasks (list[Task]): The collection of tasks to be displayed.
        """

        if not tasks:
            print("📭 No tasks found.")
            return

        print(f"{'='*10} YOUR TASKS {'='*10}")
        for task in tasks:
            print(Printer._format_task(task))
        print(f"{'='*32}")
