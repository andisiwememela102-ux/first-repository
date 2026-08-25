import sqlite3


DATABASE_NAME = "ebookstore.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    """Create the book and author tables if they do not already exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                FOREIGN KEY (authorID) REFERENCES author(id)
            )
        """)


def populate_database():
    authors = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K. Rowling", "England"),
        (2356, "C.S. Lewis", "Ireland"),
        (6380, "J.R.R. Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England")
    ]

    books = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12)
    ]

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.executemany("""
            INSERT OR IGNORE INTO author (id, name, country)
            VALUES (?, ?, ?)
        """, authors)

        cursor.executemany("""
            INSERT OR IGNORE INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
        """, books)

        conn.commit()

def get_four_digit_number(prompt):
    while True:
        value = input(prompt).strip()

        if value.isdigit() and len(value) == 4:
            return int(value)

        print("Please enter exactly four digits.")


def get_quantity(prompt):
    while True:
        value = input(prompt).strip()

        try:
            quantity = int(value)

            if quantity >= 0:
                return quantity

            print("Quantity cannot be negative.")

        except ValueError:
            print("Please enter a valid number.")


def enter_book():
    """Add a new book to the database."""
    book_id = get_four_digit_number("Enter book ID: ")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM book WHERE id = ?", (book_id,))

        if cursor.fetchone():
            print("A book with that ID already exists.")
            return

    title = input("Enter book title: ").strip()

    if not title:
        print("Book title cannot be empty.")
        return

    author_id = get_four_digit_number("Enter author ID: ")
    quantity = get_quantity("Enter quantity: ")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM author WHERE id = ?",
            (author_id,)
        )

        if cursor.fetchone() is None:
            print("Author ID does not exist.")
            return

        cursor.execute("""
            INSERT INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
        """, (book_id, title, author_id, quantity))

    print("Book added successfully.")


def update_book():
    book_id = get_four_digit_number("Enter the book ID to update: ")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT book.title, book.qty, author.name, author.country
            FROM book
            INNER JOIN author ON book.authorID = author.id
            WHERE book.id = ?
        """, (book_id,))

        book = cursor.fetchone()

        if book is None:
            print("Book not found.")
            return

        current_title, current_qty, author_name, author_country = book

        print("\nCurrent book details:")
        print(f"Title: {current_title}")
        print(f"Quantity: {current_qty}")
        print(f"Author: {author_name}")
        print(f"Country: {author_country}")

        print("\nWhat would you like to update?")
        print("1. Quantity")
        print("2. Title")
        print("3. Author")
        print("0. Cancel")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            new_quantity = get_quantity("Enter new quantity: ")

            cursor.execute("""
                UPDATE book
                SET qty = ?
                WHERE id = ?
            """, (new_quantity, book_id))

            print("Quantity updated successfully.")

        elif choice == "2":
            new_title = input("Enter new title: ").strip()

            if not new_title:
                print("Title cannot be empty.")
                return

            cursor.execute("""
                UPDATE book
                SET title = ?
                WHERE id = ?
            """, (new_title, book_id))

            print("Title updated successfully.")

        elif choice == "3":
            print(f"Current author: {author_name}")
            print(f"Current country: {author_country}")

            new_name = input(
                "Enter new author name "
                "(press Enter to keep current): "
            ).strip()

            new_country = input(
                "Enter new author country "
                "(press Enter to keep current): "
            ).strip()

            if not new_name:
                new_name = author_name

            if not new_country:
                new_country = author_country

            cursor.execute("""
                UPDATE author
                SET name = ?, country = ?
                WHERE id = (
                    SELECT authorID
                    FROM book
                    WHERE id = ?
                )
            """, (new_name, new_country, book_id))

            print("Author information updated successfully.")

        elif choice == "0":
            print("Update cancelled.")

        else:
            print("Invalid option.")


def delete_book():
    """Delete a book from the database."""
    book_id = get_four_digit_number("Enter the book ID to delete: ")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT title FROM book WHERE id = ?",
            (book_id,)
        )

        book = cursor.fetchone()

        if book is None:
            print("Book not found.")
            return

        print(f"Book found: {book[0]}")

        confirmation = input(
            "Are you sure you want to delete this book? (y/n): "
        ).strip().lower()

        if confirmation == "y":
            cursor.execute(
                "DELETE FROM book WHERE id = ?",
                (book_id,)
            )

            print("Book deleted successfully.")
        else:
            print("Deletion cancelled.")


# Search books by ID or title
def search_books():
    print("\nSearch by:")
    print("1. Book ID")
    print("2. Title")

    choice = input("Enter your choice: ").strip()

    with get_connection() as conn:
        cursor = conn.cursor()

        if choice == "1":
            book_id = get_four_digit_number("Enter book ID: ")

            cursor.execute("""
                SELECT book.id, book.title, author.name,
                       author.country, book.qty
                FROM book
                INNER JOIN author ON book.authorID = author.id
                WHERE book.id = ?
            """, (book_id,))

        elif choice == "2":
            title = input("Enter title or part of title: ").strip()

            cursor.execute("""
                SELECT book.id, book.title, author.name,
                       author.country, book.qty
                FROM book
                INNER JOIN author ON book.authorID = author.id
                WHERE book.title LIKE ?
            """, (f"%{title}%",))

        else:
            print("Invalid option.")
            return

        results = cursor.fetchall()

        if not results:
            print("No books found.")
            return

        print("\nSearch Results")
        print("-" * 50)

        for book in results:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Country: {book[3]}")
            print(f"Quantity: {book[4]}")
            print("-" * 50)


def view_all_books():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author ON book.authorID = author.id
            ORDER BY book.id
        """)

        books = cursor.fetchall()

    if not books:
        print("There are no books in the database.")
        return

    print("\nDetails")
    print("-" * 50)

    for title, author_name, country in books:
        print(f"Title: {title}")
        print(f"Author's Name: {author_name}")
        print(f"Author's Country: {country}")
        print("-" * 50)


def display_menu():
    print("\n" + "=" * 40)
    print("           SHELF TRACK")
    print("=" * 40)
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. View details of all books")
    print("0. Exit")
    print("=" * 40)


def main():
    create_tables()
    populate_database()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                enter_book()

            elif choice == "2":
                update_book()

            elif choice == "3":
                delete_book()

            elif choice == "4":
                search_books()

            elif choice == "5":
                view_all_books()

            elif choice == "0":
                print("Thank you for using Shelf Track.")
                break

            else:
                print("Invalid choice. Please select an option from 0 to 5.")

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        except Exception as error:
            print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()