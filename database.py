# Import sqlite3 which allows Python to interact with SQLite databases
import sqlite3


# -----------------------------
# FUNCTION: Connect to database
# -----------------------------
# Creates a connection to the students database file
def connect_db():

    # Connect to the database file
    conn = sqlite3.connect("students.db")

    # Configure row factory to return results as dictionaries
    conn.row_factory = sqlite3.Row

    return conn


# -----------------------------
# FUNCTION: Get all students
# -----------------------------
# Retrieves every student record stored in the database
def get_students():

    # Connect to the database
    conn = connect_db()

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Execute SQL query to retrieve all students
    cursor.execute("SELECT * FROM students")

    # Fetch all rows returned by the query
    rows = cursor.fetchall()

    # Convert rows into dictionary format
    students = [dict(row) for row in rows]

    # Close database connection
    conn.close()

    # Return student list
    return students


# -----------------------------
# FUNCTION: Add a new student
# -----------------------------
# Inserts a new student record into the database
def add_student(name, age, major):

    # Connect to the database
    conn = connect_db()

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # SQL query to insert student data
    cursor.execute(
        "INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
        (name, age, major)
    )

    # Save the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()