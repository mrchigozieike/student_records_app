# student_records.py
# Core business logic for student records management

from database import get_db_connection
from datetime import datetime

# ===================================================
# STUDENT FUNCTIONS
# ===================================================

def add_student(name, major, enrollment_date, birth_date):
    """Add a new student to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO students (name, major, enrollment_date, birth_date) 
            VALUES (?, ?, ?, ?)
        """, (name, major, enrollment_date, birth_date))
        
        student_id = cursor.lastrowid
        conn.commit()
        return {"success": True, "student_id": student_id, "message": "Student added successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}
    finally:
        conn.close()

def get_all_students():
    """Retrieve all students"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students ORDER BY student_id")
    students = cursor.fetchall()
    conn.close()
    
    return [dict(student) for student in students]

def get_student_by_id(student_id):
    """Retrieve a specific student by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    
    return dict(student) if student else None

def update_student(student_id, name, major, enrollment_date, birth_date):
    """Update student information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE students 
            SET name = ?, major = ?, enrollment_date = ?, birth_date = ?
            WHERE student_id = ?
        """, (name, major, enrollment_date, birth_date, student_id))
        
        conn.commit()
        return {"success": True, "message": "Student updated successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}
    finally:
        conn.close()

def delete_student(student_id):
    """Delete a student from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name FROM students WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            return {"success": False, "message": "Student not found"}
        
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        return {"success": True, "message": "Student deleted successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}
    finally:
        conn.close()

# ===================================================
# COURSE FUNCTIONS
# ===================================================

def add_course(course_name, start_date, end_date):
    """Add a new course"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO courses (course_name, start_date, end_date) 
            VALUES (?, ?, ?)
        """, (course_name, start_date, end_date))
        
        course_id = cursor.lastrowid
        conn.commit()
        return {"success": True, "course_id": course_id, "message": "Course added successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}
    finally:
        conn.close()

def get_all_courses():
    """Retrieve all courses"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM courses ORDER BY course_id")
    courses = cursor.fetchall()
    conn.close()
    
    return [dict(course) for course in courses]

# ===================================================
# ENROLLMENT FUNCTIONS
# ===================================================

def enroll_student(student_id, course_id, grade):
    """Enroll a student in a course"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO enrollments (student_id, course_id, grade) 
            VALUES (?, ?, ?)
        """, (student_id, course_id, grade))
        
        enrollment_id = cursor.lastrowid
        conn.commit()
        return {"success": True, "enrollment_id": enrollment_id, "message": "Student enrolled successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}
    finally:
        conn.close()

def get_all_enrollments():
    """Retrieve all enrollments with student and course details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.enrollment_id, s.name as student_name, s.student_id,
               c.course_name, c.course_id, e.grade, e.enrollment_date
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        ORDER BY e.enrollment_date DESC
    """)
    
    enrollments = cursor.fetchall()
    conn.close()
    
    return [dict(enrollment) for enrollment in enrollments]

def update_grade(enrollment_id, new_grade):
    """Update a student's grade for a course"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE enrollments 
            SET grade = ? 
            WHERE enrollment_id = ?
        """, (new_grade, enrollment_id))
        
        conn.commit()
        return {"success": True, "message": "Grade updated successfully"}
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}
    finally:
        conn.close()

# ===================================================
# DATE/TIME FILTERING FUNCTIONS
# ===================================================

def filter_students_by_date_range(start_date, end_date):
    """Filter students by enrollment date range"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT student_id, name, major, enrollment_date, birth_date
        FROM students 
        WHERE enrollment_date BETWEEN ? AND ?
        ORDER BY enrollment_date
    """, (start_date, end_date))
    
    students = cursor.fetchall()
    conn.close()
    
    return [dict(student) for student in students]

def filter_enrollments_by_date_range(start_date, end_date):
    """Filter enrollments by date range"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.enrollment_id, s.name as student_name, c.course_name, 
               e.grade, e.enrollment_date
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE date(e.enrollment_date) BETWEEN ? AND ?
        ORDER BY e.enrollment_date
    """, (start_date, end_date))
    
    enrollments = cursor.fetchall()
    conn.close()
    
    return [dict(enrollment) for enrollment in enrollments]

def get_recent_enrollments():
    """Get enrollments from the last 7 days"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.name as student_name, c.course_name, e.enrollment_date, e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.enrollment_date >= datetime('now', '-7 days')
        ORDER BY e.enrollment_date DESC
    """)
    
    enrollments = cursor.fetchall()
    conn.close()
    
    return [dict(enrollment) for enrollment in enrollments]

def get_students_by_birth_month(month):
    """Get students born in a specific month"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT student_id, name, major, birth_date
        FROM students
        WHERE strftime('%m', birth_date) = ?
        ORDER BY birth_date
    """, (month.zfill(2),))
    
    students = cursor.fetchall()
    conn.close()
    
    return [dict(student) for student in students]

def get_courses_by_date_range(start_date, end_date):
    """Get courses active within a date range"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT course_id, course_name, start_date, end_date
        FROM courses
        WHERE start_date >= ? AND end_date <= ?
        ORDER BY start_date
    """, (start_date, end_date))
    
    courses = cursor.fetchall()
    conn.close()
    
    return [dict(course) for course in courses]

# ===================================================
# JOIN FUNCTIONS - Demonstrating Table Joins
# ===================================================

def get_students_with_professors():
    """JOIN between students and professors through advising table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        s.student_id,
        s.name AS student_name,
        s.major,
        p.professor_id,
        p.name AS professor_name,
        p.email AS professor_email,
        d.department_name,
        a.start_date AS advising_start,
        a.status
    FROM students s
    INNER JOIN advising a ON s.student_id = a.student_id
    INNER JOIN professors p ON a.professor_id = p.professor_id
    INNER JOIN departments d ON p.department_id = d.department_id
    ORDER BY s.name
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_courses_with_professors():
    """JOIN between courses and professors through course_assignments"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        c.course_id,
        c.course_name,
        c.start_date,
        c.end_date,
        p.professor_id,
        p.name AS professor_name,
        p.email AS professor_email,
        ca.semester,
        ca.year,
        d.department_name
    FROM courses c
    LEFT JOIN course_assignments ca ON c.course_id = ca.course_id
    LEFT JOIN professors p ON ca.professor_id = p.professor_id
    LEFT JOIN departments d ON p.department_id = d.department_id
    ORDER BY c.course_name
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_professors_with_departments():
    """JOIN between professors and departments with aggregation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        d.department_id,
        d.department_name,
        d.building,
        d.budget,
        d.dean_name,
        p.professor_id,
        p.name AS professor_name,
        p.email,
        p.hire_date,
        p.salary,
        COUNT(DISTINCT ca.course_id) AS courses_teaching,
        COUNT(DISTINCT a.student_id) AS students_advising
    FROM departments d
    INNER JOIN professors p ON d.department_id = p.department_id
    LEFT JOIN course_assignments ca ON p.professor_id = ca.professor_id
    LEFT JOIN advising a ON p.professor_id = a.professor_id
    GROUP BY p.professor_id
    ORDER BY d.department_name, p.name
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_department_statistics():
    """JOIN across departments, professors, students, and courses"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        d.department_id,
        d.department_name,
        d.building,
        d.budget,
        COUNT(DISTINCT p.professor_id) AS professor_count,
        COUNT(DISTINCT s.student_id) AS student_count,
        COUNT(DISTINCT c.course_id) AS course_count,
        AVG(p.salary) AS avg_professor_salary,
        AVG(e.grade) AS avg_student_grade
    FROM departments d
    LEFT JOIN professors p ON d.department_id = p.department_id
    LEFT JOIN course_assignments ca ON p.professor_id = ca.professor_id
    LEFT JOIN courses c ON ca.course_id = c.course_id
    LEFT JOIN enrollments e ON c.course_id = e.course_id
    LEFT JOIN students s ON e.student_id = s.student_id AND s.major = d.department_name
    GROUP BY d.department_id
    ORDER BY d.department_name
    """)
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_student_full_details(student_id):
    """Comprehensive JOIN across all tables for a specific student"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get student basic info with advisor
    cursor.execute("""
    SELECT 
        s.student_id,
        s.name AS student_name,
        s.major,
        s.enrollment_date,
        s.birth_date,
        p.professor_id,
        p.name AS advisor_name,
        p.email AS advisor_email,
        d.department_name AS advisor_department,
        a.start_date AS advising_start,
        a.status AS advising_status
    FROM students s
    LEFT JOIN advising a ON s.student_id = a.student_id AND a.status = 'Active'
    LEFT JOIN professors p ON a.professor_id = p.professor_id
    LEFT JOIN departments d ON p.department_id = d.department_id
    WHERE s.student_id = ?
    """, (student_id,))
    
    student_info = cursor.fetchone()
    
    # Get student's enrolled courses with professor info
    cursor.execute("""
    SELECT 
        c.course_id,
        c.course_name,
        c.start_date,
        c.end_date,
        e.grade,
        e.enrollment_date,
        p.professor_id,
        p.name AS professor_name,
        p.email AS professor_email
    FROM enrollments e
    INNER JOIN courses c ON e.course_id = c.course_id
    LEFT JOIN course_assignments ca ON c.course_id = ca.course_id
    LEFT JOIN professors p ON ca.professor_id = p.professor_id
    WHERE e.student_id = ?
    ORDER BY c.course_name
    """, (student_id,))
    
    courses = cursor.fetchall()
    conn.close()
    
    return {
        "student_info": dict(student_info) if student_info else None,
        "enrolled_courses": [dict(course) for course in courses]
    }

def get_professor_workload(professor_id):
    """JOIN to get professor's teaching load and advising load"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        p.professor_id,
        p.name AS professor_name,
        p.email,
        p.hire_date,
        p.salary,
        d.department_name,
        COUNT(DISTINCT ca.course_id) AS courses_teaching,
        COUNT(DISTINCT ca.assignment_id) AS assignments_count,
        COUNT(DISTINCT a.student_id) AS students_advising,
        GROUP_CONCAT(DISTINCT c.course_name) AS courses_list,
        GROUP_CONCAT(DISTINCT s.name) AS advisees_list
    FROM professors p
    INNER JOIN departments d ON p.department_id = d.department_id
    LEFT JOIN course_assignments ca ON p.professor_id = ca.professor_id
    LEFT JOIN courses c ON ca.course_id = c.course_id
    LEFT JOIN advising a ON p.professor_id = a.professor_id AND a.status = 'Active'
    LEFT JOIN students s ON a.student_id = s.student_id
    WHERE p.professor_id = ?
    GROUP BY p.professor_id
    """, (professor_id,))
    
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def get_department_courses_with_professors(department_id):
    """JOIN to get all courses in a department with assigned professors"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        c.course_id,
        c.course_name,
        c.start_date,
        c.end_date,
        p.professor_id,
        p.name AS professor_name,
        p.email AS professor_email,
        ca.semester,
        ca.year
    FROM courses c
    LEFT JOIN course_assignments ca ON c.course_id = ca.course_id
    LEFT JOIN professors p ON ca.professor_id = p.professor_id
    WHERE p.department_id = ? OR p.department_id IS NULL
    ORDER BY c.course_name
    """, (department_id,))
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]