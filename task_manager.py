
from datetime import date, datetime
from pathlib import Path


USER_FILE = Path("user.txt")
TASK_FILE = Path("tasks.txt")
TASK_REPORT = Path("task_overview.txt")
USER_REPORT = Path("user_overview.txt")


def initialise_files():
    """Create the required data files if they do not exist."""
    if not USER_FILE.exists():
        USER_FILE.write_text("admin, adm1n\n", encoding="utf-8")

    if not TASK_FILE.exists():
        TASK_FILE.touch()


def read_users():
    users = {}

    try:
        with USER_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or "," not in line:
                    continue

                username, password = line.split(",", 1)
                username = username.strip()
                password = password.strip()

                if username:
                    users[username] = password

    except OSError as error:
        print(f"Error reading user file: {error}")

    return users


def read_tasks():
    tasks = []

    try:
        with TASK_FILE.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.rstrip("\n")

                if not line.strip():
                    continue

                parts = [part.strip() for part in line.split(", ")]

                # Split only into six fields when descriptions contain commas.
                if len(parts) > 6:
                    parts = [
                        parts[0],
                        parts[1],
                        ", ".join(parts[2:-3]),
                        parts[-3],
                        parts[-2],
                        parts[-1],
                    ]

                if len(parts) != 6:
                    print(
                        f"Warning: skipping malformed task on line "
                        f"{line_number}."
                    )
                    continue

                tasks.append(
                    {
                        "username": parts[0],
                        "title": parts[1],
                        "description": parts[2],
                        "assigned_date": parts[3],
                        "due_date": parts[4],
                        "completed": parts[5].capitalize(),
                    }
                )

    except OSError as error:
        print(f"Error reading task file: {error}")

    return tasks


def write_tasks(tasks):
    """Write all tasks back to tasks.txt."""
    try:
        with TASK_FILE.open("w", encoding="utf-8") as file:
            for task in tasks:
                file.write(
                    f"{task['username']}, {task['title']}, "
                    f"{task['description']}, {task['assigned_date']}, "
                    f"{task['due_date']}, {task['completed']}\n"
                )
    except OSError as error:
        print(f"Error writing task file: {error}")


def parse_date(date_text):
    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        return None


def get_due_date():
    """Enter until a valid current/future YYYY-MM-DD date is supplied."""
    while True:
        due_date = input("Enter the due date (YYYY-MM-DD): ").strip()
        parsed_date = parse_date(due_date)

        if parsed_date is not None and parsed_date >= date.today():
            return due_date

        print(
            "Invalid date. Please enter today's date or a future date "
            "in YYYY-MM-DD format."
        )


def login():
    users = read_users()

    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username not in users:
            print("Error: username not found. Please try again.\n")
        elif users[username] != password:
            print("Error: incorrect password. Please try again.\n")
        else:
            print(f"\nLogin successful. Welcome, {username}!\n")
            return username


def reg_user():
    users = read_users()

    while True:
        username = input("Enter a new username: ").strip()

        if not username:
            print("Username cannot be blank.")
            continue

        if "," in username:
            print("Username cannot contain a comma.")
            continue

        if username in users:
            print("That username already exists. Please choose another.")
            continue

        break

    while True:
        password = input("Enter a password: ").strip()
        confirm_password = input("Confirm the password: ").strip()

        if password != confirm_password:
            print("Passwords do not match. Please try again.")
        elif not password:
            print("Password cannot be blank.")
        else:
            break

    try:
        with USER_FILE.open("a", encoding="utf-8") as file:
            file.write(f"{username}, {password}\n")
        print(f"User '{username}' registered successfully.")
    except OSError as error:
        print(f"Error registering user: {error}")


def add_task():
    users = read_users()

    while True:
        username = input(
            "Enter the username of the person assigned to the task: "
        ).strip()

        if username in users:
            break

        print("That username does not exist. Please enter a valid user.")

    title = input("Enter the task title: ").strip()
    while not title:
        print("Task title cannot be blank.")
        title = input("Enter the task title: ").strip()

    description = input("Enter the task description: ").strip()
    while not description:
        print("Task description cannot be blank.")
        description = input("Enter the task description: ").strip()

    due_date = get_due_date()
    assigned_date = date.today().isoformat()

    task = {
        "username": username,
        "title": title,
        "description": description,
        "assigned_date": assigned_date,
        "due_date": due_date,
        "completed": "No",
    }

    tasks = read_tasks()
    tasks.append(task)
    write_tasks(tasks)

    print("Task added successfully.")


def display_task(task, number=None):
    """Display one task in a readable format."""
    if number is not None:
        print(f"\nTask {number}")
        print("-" * 50)

    print(f"Assigned to : {task['username']}")
    print(f"Title       : {task['title']}")
    print(f"Description : {task['description']}")
    print(f"Assigned    : {task['assigned_date']}")
    print(f"Due date    : {task['due_date']}")
    print(f"Completed   : {task['completed']}")


def view_all():
    """Display all tasks."""
    tasks = read_tasks()

    if not tasks:
        print("No tasks are currently recorded.")
        return

    print("\n========== ALL TASKS ==========")
    for number, task in enumerate(tasks, start=1):
        display_task(task, number)
    print()


def get_valid_task_number(task_numbers, allow_return=True):
    choice = input(
        "Enter the task number to select it"
        + (" or -1 to return: " if allow_return else ": ")
    ).strip()

    try:
        number = int(choice)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_valid_task_number(task_numbers, allow_return)

    if allow_return and number == -1:
        return -1

    if number in task_numbers:
        return number

    print("That task number does not exist. Please try again.")
    return get_valid_task_number(task_numbers, allow_return)


def complete_task(tasks, task_index):
    tasks[task_index]["completed"] = "Yes"
    write_tasks(tasks)
    print("Task marked as complete.")


def edit_task(tasks, task_index):
    task = tasks[task_index]

    if task["completed"] == "Yes":
        print("Completed tasks cannot be edited.")
        return

    users = read_users()

    while True:
        print("\nWhat would you like to edit?")
        print("1 - Assigned username")
        print("2 - Due date")
        print("3 - Both")
        print("4 - Cancel")

        choice = input("Select an option: ").strip().lower()

        if choice in {"1", "3"}:
            while True:
                username = input(
                    "Enter the new assigned username: "
                ).strip()

                if username in users:
                    task["username"] = username
                    break

                print("That username does not exist.")

        if choice in {"2", "3"}:
            task["due_date"] = get_due_date()

        if choice in {"1", "2", "3"}:
            write_tasks(tasks)
            print("Task updated successfully.")
            return

        if choice == "4":
            print("Edit cancelled.")
            return

        print("Invalid option. Please choose 1, 2, 3 or 4.")


def view_mine(current_user):
    while True:
        tasks = read_tasks()

        indexed_tasks = [
            (index, task)
            for index, task in enumerate(tasks)
            if task["username"] == current_user
        ]

        if not indexed_tasks:
            print("You have no tasks assigned to you.")
            return

        print("\n========== MY TASKS ==========")
        for number, (_, task) in enumerate(indexed_tasks, start=1):
            display_task(task, number)

        selected_number = get_valid_task_number(
            range(1, len(indexed_tasks) + 1)
        )

        if selected_number == -1:
            return

        task_index, selected_task = indexed_tasks[selected_number - 1]

        print("\nSelected task:")
        display_task(selected_task)

        while True:
            print("\n1 - Mark task as complete")
            print("2 - Edit task")
            print("3 - Return to my tasks")

            action = input("Select an option: ").strip()

            if action == "1":
                if selected_task["completed"] == "Yes":
                    print("This task is already complete.")
                else:
                    complete_task(tasks, task_index)
                break

            if action == "2":
                edit_task(tasks, task_index)
                break

            if action == "3":
                break

            print("Invalid option. Please choose 1, 2 or 3.")


def view_completed():
    tasks = read_tasks()
    completed_tasks = [
        task for task in tasks if task["completed"] == "Yes"
    ]

    if not completed_tasks:
        print("There are no completed tasks.")
        return

    print("\n========== COMPLETED TASKS ==========")
    for number, task in enumerate(completed_tasks, start=1):
        display_task(task, number)
    print()


def delete_task():
    tasks = read_tasks()

    if not tasks:
        print("There are no tasks to delete.")
        return

    print("\n========== DELETE TASK ==========")
    for number, task in enumerate(tasks, start=1):
        print(
            f"{number}. {task['title']} "
            f"(assigned to {task['username']})"
        )

    selected_number = get_valid_task_number(
        range(1, len(tasks) + 1)
    )

    if selected_number == -1:
        return

    task = tasks[selected_number - 1]
    print(f"\nYou selected: {task['title']}")

    confirmation = input(
        "Type 'yes' to permanently delete this task: "
    ).strip().lower()

    if confirmation == "yes":
        tasks.pop(selected_number - 1)
        write_tasks(tasks)
        print("Task deleted successfully.")
    else:
        print("Deletion cancelled.")


def calculate_statistics(tasks):
    total = len(tasks)
    completed = sum(task["completed"] == "Yes" for task in tasks)
    incomplete = total - completed

    overdue = 0
    today = date.today()

    for task in tasks:
        due_date = parse_date(task["due_date"])
        if (
            task["completed"] != "Yes"
            and due_date is not None
            and due_date < today
        ):
            overdue += 1

    incomplete_percentage = (
        (incomplete / total) * 100 if total else 0
    )
    overdue_percentage = (
        (overdue / total) * 100 if total else 0
    )

    return (
        total,
        completed,
        incomplete,
        overdue,
        incomplete_percentage,
        overdue_percentage,
    )


def generate_reports():
    users = read_users()
    tasks = read_tasks()

    (
        total,
        completed,
        incomplete,
        overdue,
        incomplete_percentage,
        overdue_percentage,
    ) = calculate_statistics(tasks)

    task_report = (
        "TASK OVERVIEW\n"
        "=============\n"
        f"Total number of tasks: {total}\n"
        f"Completed tasks: {completed}\n"
        f"Uncompleted tasks: {incomplete}\n"
        f"Overdue uncompleted tasks: {overdue}\n"
        f"Percentage of tasks incomplete: {incomplete_percentage:.2f}%\n"
        f"Percentage of tasks overdue: {overdue_percentage:.2f}%\n"
    )

    user_report_lines = [
        "USER OVERVIEW",
        "=============",
        f"Total number of registered users: {len(users)}",
        f"Total number of tasks: {total}",
        "",
    ]

    for username in users:
        user_tasks = [
            task for task in tasks if task["username"] == username
        ]

        user_total = len(user_tasks)
        user_completed = sum(
            task["completed"] == "Yes" for task in user_tasks
        )
        user_incomplete = user_total - user_completed

        user_overdue = 0
        today = date.today()

        for task in user_tasks:
            due_date = parse_date(task["due_date"])
            if (
                task["completed"] != "Yes"
                and due_date is not None
                and due_date < today
            ):
                user_overdue += 1

        assigned_percentage = (
            (user_total / total) * 100 if total else 0
        )
        completed_percentage = (
            (user_completed / user_total) * 100
            if user_total else 0
        )
        incomplete_percentage_user = (
            (user_incomplete / user_total) * 100
            if user_total else 0
        )
        overdue_percentage_user = (
            (user_overdue / user_total) * 100
            if user_total else 0
        )

        user_report_lines.extend(
            [
                f"User: {username}",
                f"  Tasks assigned: {user_total}",
                f"  Percentage of total tasks: "
                f"{assigned_percentage:.2f}%",
                f"  Percentage completed: "
                f"{completed_percentage:.2f}%",
                f"  Percentage still incomplete: "
                f"{incomplete_percentage_user:.2f}%",
                f"  Percentage incomplete and overdue: "
                f"{overdue_percentage_user:.2f}%",
                "",
            ]
        )

    try:
        TASK_REPORT.write_text(task_report, encoding="utf-8")
        USER_REPORT.write_text(
            "\n".join(user_report_lines),
            encoding="utf-8",
        )
        print("Reports generated successfully.")
    except OSError as error:
        print(f"Error generating reports: {error}")


def display_statistics():
    """Generate missing reports."""
    if not TASK_REPORT.exists() or not USER_REPORT.exists():
        print("Reports do not exist yet. Generating them now...")
        generate_reports()

    print("\n========== TASK STATISTICS ==========")
    try:
        print(TASK_REPORT.read_text(encoding="utf-8"))
    except OSError as error:
        print(f"Error reading task report: {error}")

    print("\n========== USER STATISTICS ==========")
    try:
        print(USER_REPORT.read_text(encoding="utf-8"))
    except OSError as error:
        print(f"Error reading user report: {error}")


def display_admin_menu():
    """Display the menu available to the admin user."""
    print("\nPlease select one of the following options:")
    print("r  - register user")
    print("a  - add task")
    print("va - view all tasks")
    print("vm - view my tasks")
    print("vc - view completed tasks")
    print("del - delete a task")
    print("ds - display statistics")
    print("gr - generate reports")
    print("e  - exit")


def display_user_menu():
    print("\nPlease select one of the following options:")
    print("a  - add task")
    print("va - view all tasks")
    print("vm - view my tasks")
    print("e  - exit")


def main():
    initialise_files()

    print("=" * 50)
    print("             TASK MANAGER")
    print("=" * 50)

    current_user = login()
    is_admin = current_user == "admin"

    while True:
        if is_admin:
            display_admin_menu()
        else:
            display_user_menu()

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "r":
            # Only the admin account may register new users.
            if is_admin:
                reg_user()
            else:
                print("Only the admin user may register users.")

        elif choice == "a":
            add_task()

        elif choice =="va":
            view_all()

        elif choice == "vm":
            view_mine(current_user)

        elif choice == "vc":
            view_completed() 

        elif choice == "del":
            delete_task()

        elif choice == "ds":
            display_statistics()

        elif choice == "gr":
            generate_reports()

        elif choice == "e":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose an option from the menu.")


if __name__ == "__main__":
    main()
