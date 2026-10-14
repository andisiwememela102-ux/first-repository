"""Tests for safe JSON file persistence."""

import tempfile
import unittest
from pathlib import Path

from src.task_manager.repository import FileTaskRepository


class TestFileTaskRepository(unittest.TestCase):
    """Check repository behaviour when its JSON file is missing or invalid."""

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = FileTaskRepository(Path(directory) / "tasks.json")
            self.assertEqual(repository.get_tasks(), [])

    def test_empty_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tasks.json"
            filename.write_text("", encoding="utf-8")
            repository = FileTaskRepository(filename)
            self.assertEqual(repository.get_tasks(), [])

    def test_malformed_json_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tasks.json"
            filename.write_text("{not valid json", encoding="utf-8")
            repository = FileTaskRepository(filename)
            self.assertEqual(repository.get_tasks(), [])


if __name__ == "__main__":
    unittest.main()
