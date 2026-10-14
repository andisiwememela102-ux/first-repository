"""Data models used by the task manager."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represent a single task."""

    task_id: int
    title: str
    description: str
    completed: bool = False

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True
