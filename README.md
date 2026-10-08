# Task Manager – OOP Modules

This project implements the OOP – Modules practical task.

## Features

- Modular Python project structure
- File-based JSON persistence
- Task creation
- Task listing
- Task completion
- Task deletion
- Unit tests for core business logic
- PEP 8 linting with Flake8
- Virtual environment support

## Project structure

```text
task_manager_oop_modules/
├── src/
│   └── task_manager/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── constants.py
│       ├── models.py
│       ├── repository.py
│       └── service.py
├── tests/
│   └── test_service.py
├── data/
├── main.py
├── .flake8
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

Windows:

```text
python -m venv .venv
.venv\Scripts\activate
pip install flake8
```

Linux/macOS:

```text
python3 -m venv .venv
source .venv/bin/activate
pip install flake8
```

## Run the application

```text
python main.py
```

## Run unit tests

```text
python -m unittest discover -s tests -v
```

## Run PEP 8 linting

```text
flake8 .
```

## Generate requirements.txt

After installing project dependencies:

```text
pip freeze > requirements.txt
```

The project itself uses Python's standard library, so requirements.txt may be
empty unless Flake8 or another development dependency is included.
