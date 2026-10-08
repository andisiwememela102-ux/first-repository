"""Business logic for the task manager."""

from .models import Task


class TaskService:
    """Provide task-management operations."""

    def __init__(self, repository):
        self.repository = repository
        self.tasks = self.repository.get_tasks()

    def add_task(self, title, description):
        """Add and persist a new task."""
        if not title.strip():
            raise ValueError("Task title cannot be empty.")

        next_id = max((task.task_id for task in self.tasks), default=0) + 1
        task = Task(next_id, title.strip(), description.strip())
        self.tasks.append(task)
        self.repository.save_tasks(self.tasks)
        return task

    def get_all_tasks(self):
        """Return all tasks."""
        return list(self.tasks)

    def complete_task(self, task_id):
        """Mark a task as completed."""
        task = self._find_task(task_id)
        task.mark_complete()
        self.repository.save_tasks(self.tasks)
        return task

    def delete_task(self, task_id):
        """Delete a task by ID."""
        task = self._find_task(task_id)
        self.tasks.remove(task)
        self.repository.save_tasks(self.tasks)

    def _find_task(self, task_id):
        """Find a task or raise an error."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise ValueError(f"Task {task_id} was not found.")
