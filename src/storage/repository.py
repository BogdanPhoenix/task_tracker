from abc import ABC, abstractmethod
from src.models.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_all(self) -> list[Task]:
        pass

    @abstractmethod
    def save_all(self, tasks: list[Task]) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Task:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> Task:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass