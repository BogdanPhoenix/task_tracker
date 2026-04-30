from abc import ABC, abstractmethod
from src.models.task import Task


class ITaskRepository(ABC):
    """
    Interface for task repository implementations.

    This abstract base class defines the standard contract for task persistence, 
    ensuring that any concrete repository implementation provides consistent 
    CRUD operations.
    """

    @abstractmethod
    def add(self, task: Task) -> Task:
        """
        Persists a new task entity.

        Args:
            task (Task): The task object to be added.

        Returns:
            Task: The persisted task instance, typically with a generated ID.
        """
        pass


    @abstractmethod
    def get_all(self) -> list[Task]:
        """
        Retrieves all task entities from the storage.

        Returns:
            list[Task]: A list containing all tasks.
        """
        pass


    @abstractmethod
    def save_all(self, tasks: list[Task]) -> None:
        """
        Persists a collection of task entities.

        Args:
            tasks (list[Task]): The list of tasks to be saved.
        """
        pass


    @abstractmethod
    def get_by_id(self, id: int) -> Task:
        """
        Retrieves a specific task by its unique identifier.

        Args:
            id (int): The identifier of the task to retrieve.

        Returns:
            Task: The requested Task instance.

        Raises:
            ValueError: If no task is found with the specified ID.
        """
        pass


    @abstractmethod
    def delete_by_id(self, id: int) -> Task:
        """
        Removes a task from storage by its identifier.

        Args:
            id (int): The identifier of the task to delete.

        Returns:
            Task: The deleted Task instance.

        Raises:
            ValueError: If no task is found with the specified ID.
        """
        pass


    @abstractmethod
    def delete_all(self) -> None:
        """
        Removes all tasks from the storage, effectively clearing it.
        """
        pass


    @abstractmethod
    def update(self, new_task: Task) -> Task:
        """
        Updates an existing task with new data.

        Args:
            new_task (Task): The task instance containing updated information.

        Returns:
            Task: The updated Task instance.

        Raises:
            ValueError: If the task to be updated is not found in storage.
        """
        pass