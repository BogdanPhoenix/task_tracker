from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


@dataclass
class Task:
    id: int
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
        self.description = new_description
        self.updated_at = datetime.now()


    def change_status(self, new_status: TaskStatus):
        self.status = new_status
        self.updated_at = datetime.now()


    def convert_to_dict(self) -> dict[str, str]:
        buffer = {
            "id": str(self.id),
            "description": self.description,
            "status": self.status.value,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }

        return buffer

    @classmethod
    def convert_from_dict(cls, obj: dict[str, str]) -> Task:
        try:
            return Task(
                id=int(obj["id"]),
                description=obj["description"],
                status=TaskStatus(obj["status"]),
                created_at=datetime.fromisoformat(obj["createdAt"]),
                updated_at=datetime.fromisoformat(obj["updatedAt"])
            )
        except (KeyError, ValueError, TypeError):
            return None

