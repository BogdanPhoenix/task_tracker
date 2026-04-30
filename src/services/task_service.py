from src.models.task import Task, TaskStatus
from src.storage.repository import ITaskRepository

class TaskService:
    """
    Service layer for managing task-related business logic.

    This class acts as an intermediary between the presentation layer (CLI) 
    and the storage layer, ensuring data validation and consistent state 
    manipulation for tasks.
    """

    def __init__(self, repository: ITaskRepository):
        """
        Initializes the TaskService with a specific repository implementation.

        Args:
            repository (ITaskRepository): The repository instance for task persistence.
        """
        self.repository = repository


    def add_task(self, description: str) -> Task:
        """
        Creates and persists a new task.

        Args:
            description (str): The textual description of the task.

        Returns:
            Task: The newly created and persisted Task object.

        Raises:
            ValueError: If the provided description is empty or whitespace only.
        """

        if not description.strip():
            raise ValueError("Description cannot be empty")

        new_task = Task(description=description)
        return self.repository.add(new_task)


    def delete_task(self, id: int) -> Task:
        """
        Removes a task from the system by its identifier.

        Args:
            id (int): The unique identifier of the task to be deleted.

        Returns:
            Task: The deleted Task object.
        """

        return self.repository.delete_by_id(id)


    def get_all_tasks(self) -> list[Task]:
        """
        Retrieves all tasks stored in the system.

        Returns:
            list[Task]: A list containing all task entities.
        """

        return self.repository.get_all()


    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        """
        Filters and retrieves tasks based on their current status.

        Args:
            status (TaskStatus): The status criteria for filtering.

        Returns:
            list[Task]: A list of tasks that match the specified status.
        """

        tasks = self.get_all_tasks()
        return [ task for task in tasks if task.status == status ]


    def get_task_by_id(self, id: int) -> Task:
        """
        Retrieves a single task by its unique identifier.

        Args:
            id (int): The identifier of the task to retrieve.

        Returns:
            Task: The requested Task object.
        """

        return self.repository.get_by_id(id)


    def update_task_description(self, id: int, description: str) -> Task:
        """
        Modifies the description of an existing task.

        Args:
            id (int): The identifier of the task to update.
            description (str): The new description for the task.

        Returns:
            Task: The updated Task object.

        Raises:
            ValueError: If the new description is empty or whitespace only.
        """

        if not description.strip():
            raise ValueError("Description cannot be empty")

        task = self.repository.get_by_id(id)
        task.change_description(description)

        return self.repository.update(task)

    def update_task_status(self, id: int, status: TaskStatus) -> Task:
        """
        Modifies the status of an existing task.

        Args:
            id (int): The identifier of the task to update.
            status (TaskStatus): The new status to be assigned.

        Returns:
            Task: The updated Task object.
        """

        task = self.repository.get_by_id(id)
        task.change_status(status)

        return self.repository.update(task)