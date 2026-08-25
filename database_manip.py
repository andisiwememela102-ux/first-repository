import sqlite3

# Connect to database(Creates student_database.db if it doesn't exist)
conn = sqlite3.connect('student_database.db')
cursor = conn.cursor()

# Create the table python_programming
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS python_programming (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade INTEGER
    )
    """
)

# Insert rows into python_programming table
students = [
    (55, "Carl Davis", 61),
    (66, "Dennis Fredrickson", 88),
    (77, "Jane Richards", 78),  
    (12, "Peyton Sawyer", 45),
    (2, "Lucas Brooke", 99),
]
cursor.executemany("""
INSERT OR REPLACE INTO python_programming (id, name, grade) VALUES (?, ?, ?)
""", 
    students ,
)

conn.commit()

# Select all records with a grade between 60 and 80
cursor.execute("""
    SELECT * FROM python_programming WHERE grade BETWEEN 60 AND 80
""")
results = cursor.fetchall()
for row in results:
    print(row)

# Change Carl Davis's grade to 65
cursor.execute("""
    UPDATE python_programming SET grade = 65 WHERE name = 'Carl Davis'
""")

conn.commit()


# Delete Dennis Fredrickson's row
cursor.execute("""
    DELETE FROM python_programming WHERE name = 'Dennis Fredrickson'
""")

conn.commit()

# Change the grade of all students with a grade greater than 55 to 80
cursor.execute("""
    UPDATE python_programming SET grade = 80 WHERE id > 55
""")

# Select and print all records from the table o see the final results
cursor.execute("""
    SELECT * FROM python_programming
""")
final_results = cursor.fetchall()
for row in final_results:
    print(row)


# Commit and Close the database connection
conn.commit()
conn.close()