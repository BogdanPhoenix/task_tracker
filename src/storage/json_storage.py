import json
import os.path

from src.models.task import Task
from src.storage.repository import ITaskRepository


class JsonTaskRepository(ITaskRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.temp_file_path = file_path + ".tmp"


    def _read_raw_data(self) -> list[dict]:
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r") as json_file:
                data = json.load(json_file)

            if not isinstance(data, list):
                return []

            return [item for item in data if isinstance(item, dict)]
        except json.JSONDecodeError:
            return []


    def get_all(self) -> list[Task]:
        data = self._read_raw_data()

        tasks = []

        for element in data:
            task = Task.convert_from_dict(element)

            if task is not None:
                tasks.append(task)

        return tasks


    def save_all(self, tasks: list[Task]) -> None:
        data = [ task.convert_to_dict() for task in tasks ]
        json_str = json.dumps(data, indent=4)

        with open(self.temp_file_path, "w") as json_file:
            json_file.write(json_str)
            json_file.flush()
            os.fsync(json_file.fileno())

        try:
            os.replace(self.temp_file_path, self.file_path)
        except OSError as e:
            os.remove(self.temp_file_path)
            raise Exception("Failed to save data") from e


    def get_by_id(self, id: int) -> Task:
        data = self._read_raw_data()

        for element in data:
            if int(element["id"]) == id:
                return Task.convert_from_dict(element)

        raise ValueError(f"Task with id = {id} not found")

    