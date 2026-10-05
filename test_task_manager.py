import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import task_manager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(self.id().replace(".", "_"))
        self.temp_dir.mkdir(exist_ok=True)

        self.user_file = self.temp_dir / "user.txt"
        self.task_file = self.temp_dir / "tasks.txt"

        self.user_file.write_text(
            "admin, adm1n\nstudent, password123\n",
            encoding="utf-8",
        )

        task_manager.USER_FILE = self.user_file
        task_manager.TASK_FILE = self.task_file

    def tearDown(self):
        for file_path in self.temp_dir.iterdir():
            file_path.unlink()
        self.temp_dir.rmdir()

    def test_parse_date_accepts_valid_date(self):
        # Arrange
        valid_date = "2026-10-20"

        # Act
        result = task_manager.parse_date(valid_date)

        # Assert
        self.assertEqual(result.isoformat(), valid_date)

    def test_parse_date_rejects_invalid_date(self):
        # Arrange
        invalid_date = "20-10-2026"

        # Act
        result = task_manager.parse_date(invalid_date)

        # Assert
        self.assertIsNone(result)

    def test_write_and_read_tasks_preserves_task_data(self):
        # Arrange
        tasks = [
            {
                "username": "student",
                "title": "Complete testing",
                "description": "Write unit tests",
                "assigned_date": "2026-10-05",
                "due_date": "2026-10-20",
                "completed": "No",
            }
        ]

        # Act
        task_manager.write_tasks(tasks)
        result = task_manager.read_tasks()

        # Assert
        self.assertEqual(result, tasks)

    def test_calculate_statistics_counts_completed_and_incomplete(self):
        # Arrange
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()

        tasks = [
            {
                "username": "student",
                "title": "Finished task",
                "description": "Done",
                "assigned_date": "2026-10-01",
                "due_date": tomorrow,
                "completed": "Yes",
            },
            {
                "username": "student",
                "title": "Incomplete task",
                "description": "Still working",
                "assigned_date": "2026-10-01",
                "due_date": tomorrow,
                "completed": "No",
            },
            {
                "username": "admin",
                "title": "Overdue task",
                "description": "Needs attention",
                "assigned_date": "2026-10-01",
                "due_date": yesterday,
                "completed": "No",
            },
        ]

        # Act
        result = task_manager.calculate_statistics(tasks)

        # Assert
        total, completed, incomplete, overdue, incomplete_pct, overdue_pct = result
        self.assertEqual(total, 3)
        self.assertEqual(completed, 1)
        self.assertEqual(incomplete, 2)
        self.assertEqual(overdue, 1)
        self.assertAlmostEqual(incomplete_pct, 66.67, places=2)
        self.assertAlmostEqual(overdue_pct, 33.33, places=2)

    def test_complete_task_marks_task_as_completed(self):
        # Arrange
        tasks = [
            {
                "username": "student",
                "title": "Testing task",
                "description": "Run tests",
                "assigned_date": "2026-10-05",
                "due_date": "2026-10-20",
                "completed": "No",
            }
        ]

        # Act
        with patch("builtins.print"):
            task_manager.complete_task(tasks, 0)

        # Assert
        self.assertEqual(tasks[0]["completed"], "Yes")
        self.assertEqual(task_manager.read_tasks(), tasks)


if __name__ == "__main__":
    unittest.main()
