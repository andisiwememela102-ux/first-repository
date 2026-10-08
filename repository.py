"""Data access layer for file-based task storage."""

import json
from pathlib import Path

from .models import Task


class FileTaskRepository:
    """Store and retrieve tasks from a JSON file."""

    def __init__(self, filename):
        self.filename = Path(filename)

    def get_tasks(self):
        """Read tasks from the JSON file."""
        if not self.filename.exists():
            return []

        with self.filename.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [Task(**item) for item in data]

    def save_tasks(self, tasks):
        """Write tasks to the JSON file."""
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        data = [task.__dict__ for task in tasks]

        with self.filename.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
