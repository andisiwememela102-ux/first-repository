"""Unit tests for task-management business logic."""

import unittest

from src.task_manager.models import Task
from src.task_manager.service import TaskService


class FakeRepository:
    """In-memory repository used to isolate unit tests from files."""

    def __init__(self):
        self.tasks = []

    def get_tasks(self):
        """Return a copy of stored tasks."""
        return list(self.tasks)

    def save_tasks(self, tasks):
        """Store a copy of the supplied tasks."""
        self.tasks = list(tasks)


class TestTaskService(unittest.TestCase):
    """Test the core task-management use cases."""

    def setUp(self):
        self.repository = FakeRepository()
        self.service = TaskService(self.repository)

    def test_add_task(self):
        """A task can be added."""
        task = self.service.add_task("Study Python", "Complete the modules task.")

        self.assertEqual(task.task_id, 1)
        self.assertEqual(len(self.service.get_all_tasks()), 1)
        self.assertEqual(task.title, "Study Python")

    def test_get_all_tasks(self):
        """All current tasks are returned."""
        self.repository.tasks = [
            Task(1, "Task one", "First task"),
            Task(2, "Task two", "Second task"),
        ]

        self.service = TaskService(self.repository)

        self.assertEqual(len(self.service.get_all_tasks()), 2)

    def test_complete_task(self):
        """A task can be marked as completed."""
        task = self.service.add_task("Finish assignment", "Complete practical task.")
        completed_task = self.service.complete_task(task.task_id)

        self.assertTrue(completed_task.completed)

    def test_delete_task(self):
        """A task can be deleted."""
        task = self.service.add_task("Remove me", "Temporary task.")
        self.service.delete_task(task.task_id)

        self.assertEqual(self.service.get_all_tasks(), [])

    def test_empty_title_is_rejected(self):
        """An empty title raises a ValueError."""
        with self.assertRaises(ValueError):
            self.service.add_task("   ", "Description")


if __name__ == "__main__":
    unittest.main()
