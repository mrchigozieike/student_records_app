import sqlite3

DATABASE = "students.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    """
    Create the students table if it does not already exist.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            major TEXT
        )
        """)

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("Database error:", e)


def insert_student(name, age, major):
    """
    Insert a new student into the database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
            (name, age, major)
        )

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("Insert error:", e)


def get_students():
    """
    Retrieve all students from the database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")

        students = cursor.fetchall()

        conn.close()

        return [dict(row) for row in students]

    except sqlite3.Error as e:
        print("Query error:", e)
        return []


def update_student(student_id, name, age, major):
    """
    Update student information.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE students SET name=?, age=?, major=? WHERE id=?",
            (name, age, major, student_id)
        )

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("Update error:", e)


def delete_student(student_id):
    """
    Delete a student from the database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("Delete error:", e)


def get_student_statistics():
    """
    Return statistics using SQL aggregate functions.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            COUNT(*) AS total_students,
            AVG(age) AS average_age
        FROM students
        """)

        stats = cursor.fetchone()

        conn.close()

        return dict(stats)

    except sqlite3.Error as e:
        print("Statistics error:", e)
        return None