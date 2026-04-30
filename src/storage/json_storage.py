import json
import os.path

from dataclasses import replace
from src.models.task import Task
from src.storage.repository import ITaskRepository


class JsonTaskRepository(ITaskRepository):
    """
    JSON-based implementation of the task repository.

    This class handles task persistence using a local JSON file. It ensures 
    atomic writes and provides methods for full CRUD operations on tasks.
    """

    def __init__(self, file_path: str):
        """
        Initializes the repository with a specific file path.

        Args:
            file_path (str): The absolute or relative path to the JSON storage file.
        """
        self.file_path = file_path
        self.temp_file_path = file_path + ".tmp"



    def _read_raw_data(self) -> list[dict]:
        """
        Reads the raw dictionary data from the JSON file.

        Returns:
            list[dict]: A list of raw task dictionaries, or an empty list if 
                        the file does not exist or is corrupted.
        """

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
        """
        Assigns a new unique ID and persists the task to the JSON file.

        Args:
            task (Task): The task entity to be persisted.

        Returns:
            Task: The persisted task instance with its assigned ID.
        """

        data = self._read_raw_data()
        new_id = max((t["id"] for t in data), default=0) + 1

        task_with_id = replace(task, id=new_id)
        data.append(task_with_id.convert_to_dict())
        self._save_json(data)

        return task_with_id


    def get_all(self) -> list[Task]:
        """
        Retrieves all tasks from the JSON file and converts them to Task objects.

        Returns:
            list[Task]: A list of all persisted task entities.
        """

        data = self._read_raw_data()

        tasks = []

        for element in data:
            task = Task.convert_from_dict(element)

            if task is not None:
                tasks.append(task)

        return tasks


    def _save_json(self, json_data: list[dict]) -> None:
        """
        Performs an atomic write operation to the JSON file.

        This method writes to a temporary file first and then replaces the 
        target file to prevent data loss in case of a crash during writing.

        Args:
            json_data (list[dict]): The raw data to be serialized and saved.

        Raises:
            Exception: If the file write or replacement operation fails.
        """

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
        """
        Converts a list of Task objects and persists them to the JSON file.

        Args:
            tasks (list[Task]): The collection of tasks to be saved.
        """

        json_data = [ task.convert_to_dict() for task in tasks ]
        self._save_json(json_data)


    def get_by_id(self, id: int) -> Task:
        """
        Locates and retrieves a specific task by its ID.

        Args:
            id (int): The unique identifier of the task.

        Returns:
            Task: The requested Task object.

        Raises:
            ValueError: If no task with the specified ID exists.
        """

        data = self._read_raw_data()

        for element in data:
            if element["id"] == id:
                return Task.convert_from_dict(element)

        raise ValueError(f"Task with id = {id} not found")


    def delete_by_id(self, id: int) -> Task:
        """
        Removes a task from the JSON storage by its ID.

        Args:
            id (int): The identifier of the task to be deleted.

        Returns:
            Task: The Task object that was removed.

        Raises:
            ValueError: If the task ID is not found.
        """

        all_elements = self._read_raw_data()

        target_index = -1
        for i, element in enumerate(all_elements):
            if element["id"] == id:
                target_index = i
                break

        if target_index == -1:
            raise ValueError(f"Task with id = {id} not found")

        removed_data = all_elements.pop(target_index)
        self._save_json(all_elements)

        return Task.convert_from_dict(removed_data)


    def delete_all(self) -> None:
        """
        Clears all data from the JSON file, resulting in an empty repository.

        Raises:
            Exception: If the clearing operation fails.
        """

        try:
            self._save_json([])
        except Exception as e:
            raise Exception(f"Unable to delete the contents of the file ‘{self.file_path}’.") from e


    def update(self, new_task: Task) -> Task:
        """
        Updates an existing task record with new information.

        Args:
            new_task (Task): The task object containing updated state.

        Returns:
            Task: The updated Task object.

        Raises:
            ValueError: If the task ID is not found in the storage.
        """

        all_elements = self._read_raw_data()

        for i, element in enumerate(all_elements):
            if element["id"] == new_task.id:
                all_elements[i] = new_task.convert_to_dict()

                self._save_json(all_elements)
                return new_task

        raise ValueError(f"Task with id = {new_task.id} not found")