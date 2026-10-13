"""Command-line interface for the task manager."""

from .config import DATA_FILE
from .repository import FileTaskRepository
from .service import TaskService


def display_tasks(tasks):
    """Display tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "Done" if task.completed else "Pending"
        print(f"{task.task_id}. {task.title} - {status}")
        print(f"   {task.description}")


def start_application():
    """Start the task manager application."""
    repository = FileTaskRepository(DATA_FILE)
    service = TaskService(repository)

    while True:
        print("\nTask Manager")
        print("1. View tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Quit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                display_tasks(service.get_all_tasks())
            elif choice == "2":
                title = input("Title: ")
                description = input("Description: ")
                service.add_task(title, description)
                print("Task added successfully.")
            elif choice == "3":
                task_id = int(input("Task ID: "))
                service.complete_task(task_id)
                print("Task marked as complete.")
            elif choice == "4":
                task_id = int(input("Task ID: "))
                service.delete_task(task_id)
                print("Task deleted successfully.")
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")
