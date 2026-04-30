from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """
    Enumeration representing the lifecycle states of a task.

    Members:
        TODO: The task is pending and has not yet been initiated.
        IN_PROGRESS: The task is currently under execution.
        DONE: The task has been successfully finalized.
    """
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


@dataclass
class Task:
    """
    Represents a task entity within the system.

    This data class encapsulates all necessary information for a task, 
    including its unique identifier, description, current status, 
    and audit timestamps for creation and last update.
    """

    id: int = 0
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = None
    updated_at: datetime = None


    def __post_init__(self):
        datetime_now = datetime.now()

        self.created_at = datetime_now if self.created_at is None else self.created_at
        self.updated_at = datetime_now if self.updated_at is None else self.updated_at


    def __eq__(self, other: Task) -> bool:
        return (self.id == other.id
                and self.description == other.description
                and self.status == other.status
                )


    def change_description(self, new_description: str):
        """
        Updates the task description and refreshes the modification timestamp.

        Args:
            new_description (str): The new textual description for the task.
        """

        self.description = new_description
        self.updated_at = datetime.now()


    def change_status(self, new_status: TaskStatus):
        """
        Updates the task status and refreshes the modification timestamp.

        Args:
            new_status (TaskStatus): The new status to be assigned to the task.
        """

        self.status = new_status
        self.updated_at = datetime.now()


    def convert_to_dict(self) -> dict:
        """
        Serializes the task object into a dictionary format.

        This method is primarily used for data persistence in JSON format, 
        ensuring dates are converted to ISO strings.

        Returns:
            dict: A dictionary representation of the task instance.
        """

        buffer = {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }

        return buffer

    @classmethod
    def convert_from_dict(cls, obj: dict) -> Task:
        """
        Deserializes a dictionary into a Task object.

        Args:
            obj (dict): The dictionary containing task data.

        Returns:
            Task: A new Task instance if successful, or None if data is invalid.
        """

        try:
            return Task(
                id=obj["id"],
                description=obj["description"],
                status=TaskStatus(obj["status"]),
                created_at=datetime.fromisoformat(obj["createdAt"]),
                updated_at=datetime.fromisoformat(obj["updatedAt"])
            )
        except (KeyError, ValueError, TypeError):
            return None

    @property
    def status_formatted(self) -> str:
        """
        Returns a human-readable, uppercase version of the task status.

        Returns:
            str: The formatted status string (e.g., "IN PROGRESS").
        """

        return self.status.value.upper().replace("-", " ")

    def __repr__(self) -> str:
        return f"Task(id={self.id}, status='{self.status.value}')"
