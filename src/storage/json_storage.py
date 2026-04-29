import json
import os.path

from dataclasses import replace
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


    def add(self, task: Task) -> Task:
        data = self._read_raw_data()
        new_id = max((int(t["id"]) for t in data), default=0) + 1

        task_with_id = replace(task, id=new_id)
        data.append(task_with_id.convert_to_dict())
        self._save_json(data)

        return task_with_id


    def get_all(self) -> list[Task]:
        data = self._read_raw_data()

        tasks = []

        for element in data:
            task = Task.convert_from_dict(element)

            if task is not None:
                tasks.append(task)

        return tasks


    def _save_json(self, json_data: list[dict]) -> None:
        json_str = json.dumps(json_data, indent=4)

        with open(self.temp_file_path, "w") as json_file:
            json_file.write(json_str)
            json_file.flush()
            os.fsync(json_file.fileno())

        try:
            os.replace(self.temp_file_path, self.file_path)
        except OSError as e:
            os.remove(self.temp_file_path)
            raise Exception("Failed to save data") from e


    def save_all(self, tasks: list[Task]) -> None:
        json_data = [ task.convert_to_dict() for task in tasks ]
        self._save_json(json_data)


    def get_by_id(self, id: int) -> Task:
        data = self._read_raw_data()

        for element in data:
            if int(element["id"]) == id:
                return Task.convert_from_dict(element)

        raise ValueError(f"Task with id = {id} not found")


    def delete_by_id(self, id: int) -> Task:
        all_elements = self._read_raw_data()

        target_index = -1
        for i, element in enumerate(all_elements):
            if int(element["id"]) == id:
                target_index = i
                break

        if target_index == -1:
            raise ValueError(f"Task with id = {id} not found")

        removed_data = all_elements.pop(target_index)
        self._save_json(all_elements)

        return Task.convert_from_dict(removed_data)


    def delete_all(self) -> None:
        try:
            self._save_json([])
        except Exception as e:
            raise Exception(f"Unable to delete the contents of the file ‘{self.file_path}’.") from e