# Student Records Management System
# CSE 310 – Applied Programming
# This program demonstrates how Python interacts with a SQL relational database
# using SQLite. The program allows the user to insert, update, delete,
# and retrieve student data.

import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect("students.db")
cursor = conn.cursor()


# ---------------------------------------------------
# Create database tables
# ---------------------------------------------------
def create_tables():
    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        major TEXT
    )
    """)

    # Courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL
    )
    """)

    # Enrollment table (links students and courses)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        grade INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(course_id) REFERENCES courses(course_id)
    )
    """)

    conn.commit()


# ---------------------------------------------------
# Add new student
# ---------------------------------------------------
def add_student():
    name = input("Enter student name: ")
    major = input("Enter student major: ")

    cursor.execute(
        "INSERT INTO students (name, major) VALUES (?, ?)",
        (name, major)
    )

    conn.commit()
    print("Student added successfully.")


# ---------------------------------------------------
# Add course
# ---------------------------------------------------
def add_course():
    course_name = input("Enter course name: ")

    cursor.execute(
        "INSERT INTO courses (course_name) VALUES (?)",
        (course_name,)
    )

    conn.commit()
    print("Course added successfully.")


# ---------------------------------------------------
# Enroll student in course
# ---------------------------------------------------
def enroll_student():
    student_id = input("Enter student ID: ")
    course_id = input("Enter course ID: ")
    grade = input("Enter grade: ")

    cursor.execute(
        "INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?)",
        (student_id, course_id, grade)
    )

    conn.commit()
    print("Student enrolled successfully.")


# ---------------------------------------------------
# View students
# ---------------------------------------------------
def view_students():
    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    print("\nStudents:")
    for student in students:
        print(student)


# ---------------------------------------------------
# View courses
# ---------------------------------------------------
def view_courses():
    cursor.execute("SELECT * FROM courses")

    courses = cursor.fetchall()

    print("\nCourses:")
    for course in courses:
        print(course)


# ---------------------------------------------------
# View enrollments with JOIN
# ---------------------------------------------------
def view_enrollments():
    cursor.execute("""
    SELECT students.name, courses.course_name, enrollments.grade
    FROM enrollments
    JOIN students ON enrollments.student_id = students.student_id
    JOIN courses ON enrollments.course_id = courses.course_id
    """)

    records = cursor.fetchall()

    print("\nStudent Enrollments:")
    for record in records:
        print(record)


# ---------------------------------------------------
# Update grade
# ---------------------------------------------------
def update_grade():
    enrollment_id = input("Enter enrollment ID: ")
    new_grade = input("Enter new grade: ")

    cursor.execute(
        "UPDATE enrollments SET grade=? WHERE enrollment_id=?",
        (new_grade, enrollment_id)
    )

    conn.commit()
    print("Grade updated successfully.")


# ---------------------------------------------------
# Delete student
# ---------------------------------------------------
def delete_student():
    student_id = input("Enter student ID to delete: ")

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()
    print("Student deleted.")


# ---------------------------------------------------
# Menu system
# ---------------------------------------------------
def menu():
    while True:
        print("\nStudent Records System")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student")
        print("4. View Students")
        print("5. View Courses")
        print("6. View Enrollments")
        print("7. Update Grade")
        print("8. Delete Student")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_course()
        elif choice == "3":
            enroll_student()
        elif choice == "4":
            view_students()
        elif choice == "5":
            view_courses()
        elif choice == "6":
            view_enrollments()
        elif choice == "7":
            update_grade()
        elif choice == "8":
            delete_student()
        elif choice == "9":
            break
        else:
            print("Invalid option.")


# ---------------------------------------------------
# Run program
# ---------------------------------------------------
create_tables()
menu()

conn.close()