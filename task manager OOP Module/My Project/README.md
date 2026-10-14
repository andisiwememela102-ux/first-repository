# Task Manager – OOP Modules

This project implements the OOP – Modules practical task.

## Features

- Modular Python project structure
- File-based JSON persistence
- Task creation
- Task listing
- Task completion
- Task deletion
- Unit tests for core business logic and invalid input
- Validation for empty and overlong task titles
- Safe handling of empty or malformed JSON data files
- PEP 8 linting with Flake8


## Notes

- Task titles must contain between 1 and 100 characters.
- Task data is saved to `data/tasks.json` (created when the first task is saved).
- If the JSON file is empty or malformed, the application starts with an empty task list rather than crashing.
- `requirements.txt` documents that the application has no third-party runtime dependencies. Flake8 is optional for development.
