# database.py
# Handles SQLite database connection and setup

import sqlite3

DATABASE = "students.db"


def get_db_connection():
    """
    Create and return a database connection
    """
    conn = sqlite3.connect(DATABASE)

    # Allows accessing columns by name
    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    """
    Create database tables if they do not exist
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Departments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # Create Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments (id)
    )
    """)

    # Insert sample departments
    cursor.execute("INSERT OR IGNORE INTO departments (id, name) VALUES (1, 'Software Development')")
    cursor.execute("INSERT OR IGNORE INTO departments (id, name) VALUES (2, 'Computer Science')")
    cursor.execute("INSERT OR IGNORE INTO departments (id, name) VALUES (3, 'Information Technology')")

    conn.commit()
    conn.close()