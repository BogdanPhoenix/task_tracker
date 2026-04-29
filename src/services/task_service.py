from src.models.task import Task, TaskStatus
from src.storage.repository import ITaskRepository

class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository


    def add_task(self, description: str) -> Task:
        if not description.strip():
            raise ValueError("Description cannot be empty")

        new_task = Task(description=description)
        return self.repository.add(new_task)


    def delete_task(self, id: int) -> Task:
        return self.repository.delete_by_id(id)


    def get_all_tasks(self) -> list[Task]:
        return self.repository.get_all()


    def get_task_by_id(self, id: int) -> Task:
        return self.repository.get_by_id(id)


    def update_task_description(self, id: int, description: str) -> Task:
        if not description.strip():
            raise ValueError("Description cannot be empty")

        task = self.repository.get_by_id(id)
        task.change_description(description)

        return self.repository.update(task)

    def update_task_status(self, id: int, status: TaskStatus) -> Task:
        task = self.repository.get_by_id(id)
        task.change_status(status)

        return self.repository.update(task)