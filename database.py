# database.py
# Handles SQLite database connection and setup

import sqlite3
import os

DATABASE = "students.db"

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Create database tables if they do not exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Students table with DATE columns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        major TEXT,
        enrollment_date DATE,
        birth_date DATE
    )
    """)
    
    # Create Courses table with DATE columns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        start_date DATE,
        end_date DATE
    )
    """)
    
    # Create Enrollments table with DATETIME column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        grade INTEGER,
        enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE
    )
    """)
    
    # ============ NEW TABLES FOR JOIN DEMONSTRATIONS ============
    
    # Create Departments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE,
        building TEXT,
        budget INTEGER,
        dean_name TEXT
    )
    """)
    
    # Create Professors table (JOIN with Departments)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professors (
        professor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        hire_date DATE,
        department_id INTEGER,
        salary INTEGER,
        FOREIGN KEY(department_id) REFERENCES departments(department_id) ON DELETE SET NULL
    )
    """)
    
    # Create Course_Assignments table (JOIN with Professors and Courses)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        professor_id INTEGER,
        course_id INTEGER,
        semester TEXT,
        year INTEGER,
        FOREIGN KEY(professor_id) REFERENCES professors(professor_id) ON DELETE CASCADE,
        FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE
    )
    """)
    
    # Create Advising table (JOIN between Professors and Students)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS advising (
        advising_id INTEGER PRIMARY KEY AUTOINCREMENT,
        professor_id INTEGER,
        student_id INTEGER,
        start_date DATE,
        end_date DATE,
        status TEXT DEFAULT 'Active',
        FOREIGN KEY(professor_id) REFERENCES professors(professor_id) ON DELETE CASCADE,
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized with DATE/TIME columns and JOIN tables (Departments, Professors, Course_Assignments, Advising)")

def reset_db():
    """Reset the database (delete all data)"""
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("Database reset successfully!")
    init_db()

def insert_sample_data():
    """Insert sample data for testing including JOIN tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert sample students with dates
        sample_students = [
            ('Alice Johnson', 'Computer Science', '2024-01-15', '2000-05-15'),
            ('Bob Smith', 'Engineering', '2024-01-20', '1999-08-22'),
            ('Carol Davis', 'Mathematics', '2024-02-01', '2001-03-10'),
            ('David Wilson', 'Physics', '2024-02-10', '2000-11-30'),
            ('Emma Brown', 'Chemistry', '2024-03-01', '1999-12-05'),
            ('Frank Miller', 'Computer Science', '2024-03-15', '2001-07-18'),
            ('Grace Lee', 'Engineering', '2024-03-20', '2000-09-25')
        ]
        
        cursor.executemany(
            "INSERT INTO students (name, major, enrollment_date, birth_date) VALUES (?, ?, ?, ?)",
            sample_students
        )
        
        # Insert sample courses with dates
        sample_courses = [
            ('Database Systems', '2024-01-10', '2024-05-20'),
            ('Web Development', '2024-01-15', '2024-05-25'),
            ('Data Structures', '2024-02-01', '2024-06-01'),
            ('Operating Systems', '2024-03-01', '2024-07-15'),
            ('Machine Learning', '2024-02-15', '2024-06-10')
        ]
        
        cursor.executemany(
            "INSERT INTO courses (course_name, start_date, end_date) VALUES (?, ?, ?)",
            sample_courses
        )
        
        # Insert sample departments
        sample_departments = [
            ('Computer Science', 'Byrd Hall 101', 5000000, 'Dr. James Wilson'),
            ('Engineering', 'Engineering Building 200', 7500000, 'Dr. Sarah Chen'),
            ('Mathematics', 'Math Sciences 305', 3000000, 'Dr. Robert Brown'),
            ('Physics', 'Physical Sciences 150', 4000000, 'Dr. Maria Garcia'),
            ('Chemistry', 'Chemistry Lab 220', 3500000, 'Dr. John Davis')
        ]
        
        cursor.executemany(
            "INSERT INTO departments (department_name, building, budget, dean_name) VALUES (?, ?, ?, ?)",
            sample_departments
        )
        
        # Insert sample professors
        sample_professors = [
            ('Dr. Alan Turing', 'turing@university.edu', '2010-08-15', 1, 120000),
            ('Dr. Ada Lovelace', 'lovelace@university.edu', '2012-01-10', 1, 115000),
            ('Dr. Nikola Tesla', 'tesla@university.edu', '2015-03-20', 2, 130000),
            ('Dr. Marie Curie', 'curie@university.edu', '2011-09-05', 4, 125000),
            ('Dr. Katherine Johnson', 'kjohnson@university.edu', '2018-06-12', 3, 110000),
            ('Dr. Albert Einstein', 'einstein@university.edu', '2008-11-01', 4, 140000),
            ('Dr. Rosalind Franklin', 'franklin@university.edu', '2016-04-18', 5, 118000)
        ]
        
        cursor.executemany(
            "INSERT INTO professors (name, email, hire_date, department_id, salary) VALUES (?, ?, ?, ?, ?)",
            sample_professors
        )
        
        # Insert sample course assignments
        sample_assignments = [
            (1, 1, 'Fall', 2024),  # Dr. Turing teaches Database Systems
            (1, 3, 'Fall', 2024),  # Dr. Turing teaches Data Structures
            (2, 2, 'Fall', 2024),  # Dr. Lovelace teaches Web Development
            (2, 5, 'Fall', 2024),  # Dr. Lovelace teaches Machine Learning
            (3, 4, 'Fall', 2024),  # Dr. Tesla teaches Operating Systems
            (4, 4, 'Fall', 2024),  # Dr. Curie teaches Operating Systems
            (5, 3, 'Fall', 2024),  # Dr. Johnson teaches Data Structures
            (6, 4, 'Fall', 2024)   # Dr. Einstein teaches Operating Systems
        ]
        
        cursor.executemany(
            "INSERT INTO course_assignments (professor_id, course_id, semester, year) VALUES (?, ?, ?, ?)",
            sample_assignments
        )
        
        # Insert sample advising relationships
        sample_advising = [
            (1, 1, '2024-01-15', None, 'Active'),   # Dr. Turing advises Alice
            (1, 3, '2024-02-01', None, 'Active'),   # Dr. Turing advises Carol
            (2, 5, '2024-03-01', None, 'Active'),   # Dr. Lovelace advises Emma
            (3, 2, '2024-01-20', None, 'Active'),   # Dr. Tesla advises Bob
            (4, 4, '2024-02-10', None, 'Active'),   # Dr. Curie advises David
            (5, 6, '2024-03-15', None, 'Active'),   # Dr. Johnson advises Frank
            (6, 7, '2024-03-20', None, 'Active')    # Dr. Einstein advises Grace
        ]
        
        cursor.executemany(
            "INSERT INTO advising (professor_id, student_id, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
            sample_advising
        )
        
        # Insert sample enrollments
        sample_enrollments = [
            (1, 1, 85), (1, 2, 90), (2, 1, 78), (3, 3, 92),
            (4, 2, 88), (5, 4, 95), (6, 5, 87), (7, 3, 84),
            (1, 4, 91), (2, 5, 86), (3, 1, 89), (4, 2, 93)
        ]
        
        cursor.executemany(
            "INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?)",
            sample_enrollments
        )
        
        conn.commit()
        print("✅ Sample data inserted with dates and JOIN tables")
    else:
        print(f"📊 Sample data already exists ({count} students found)")
    
    conn.close()