from src.models.task import Task

class Printer:
    @staticmethod
    def _format_task(task: Task) -> str:
        return f"#{task.id:<3} | [{task.status_formatted:^11}] | {task.description}"

    @staticmethod
    def success(message: str, task: Task = None) -> None:
        print(f"✅ {message}")
        if task:
            print(Printer._format_task(task))

    @staticmethod
    def error(message: str) -> None:
        print(f"❌ Error: {message}")

    @staticmethod
    def critical(message: str) -> None:
        print(f"💥 Critical Error: {message}")

    @staticmethod
    def task_list(tasks: list[Task]) -> None:
        if not tasks:
            print("📭 No tasks found.")
            return

        print(f"{'='*10} YOUR TASKS {'='*10}")
        for task in tasks:
            print(Printer._format_task(task))
        print(f"{'='*32}")
