# api.py - Main Flask App
# Student Records Management System - Web Application
# CSE 310 – Applied Programming

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, insert_sample_data, reset_db

# IMPORT ALL FUNCTIONS from student_records
from student_records import (
    # Student functions
    add_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,
    # Course functions
    add_course,
    get_all_courses,
    # Enrollment functions
    enroll_student,
    get_all_enrollments,
    update_grade,
    # Date filtering functions
    filter_students_by_date_range,
    filter_enrollments_by_date_range,
    get_recent_enrollments,
    get_students_by_birth_month,
    get_courses_by_date_range,
    # JOIN functions (new)
    get_students_with_professors,
    get_courses_with_professors,
    get_professors_with_departments,
    get_department_statistics,
    get_student_full_details,
    get_professor_workload,
    get_department_courses_with_professors
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# ===================================================
# WEB INTERFACE ROUTES (With Templates)
# ===================================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# Student Routes
@app.route('/students')
def view_students_web():
    """View all students"""
    students = get_all_students()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student_web():
    """Add a new student"""
    if request.method == 'POST':
        name = request.form['name']
        major = request.form['major']
        enrollment_date = request.form['enrollment_date']
        birth_date = request.form['birth_date']
        
        result = add_student(name, major, enrollment_date, birth_date)
        if result['success']:
            flash('Student added successfully!', 'success')
        else:
            flash('Error adding student!', 'error')
        return redirect(url_for('view_students_web'))
    
    return render_template('add_student.html')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student_web(student_id):
    """Edit a student"""
    if request.method == 'POST':
        name = request.form['name']
        major = request.form['major']
        enrollment_date = request.form['enrollment_date']
        birth_date = request.form['birth_date']
        
        result = update_student(student_id, name, major, enrollment_date, birth_date)
        if result['success']:
            flash('Student updated successfully!', 'success')
        else:
            flash('Error updating student!', 'error')
        return redirect(url_for('view_students_web'))
    
    student = get_student_by_id(student_id)
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:student_id>')
def delete_student_web(student_id):
    """Delete a student"""
    result = delete_student(student_id)
    if result['success']:
        flash('Student deleted successfully!', 'success')
    else:
        flash('Error deleting student!', 'error')
    return redirect(url_for('view_students_web'))

# Course Routes
@app.route('/courses')
def view_courses_web():
    """View all courses"""
    courses = get_all_courses()
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course_web():
    """Add a new course"""
    if request.method == 'POST':
        course_name = request.form['course_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        result = add_course(course_name, start_date, end_date)
        if result['success']:
            flash('Course added successfully!', 'success')
        else:
            flash('Error adding course!', 'error')
        return redirect(url_for('view_courses_web'))
    
    return render_template('add_course.html')

# Enrollment Routes
@app.route('/enrollments')
def view_enrollments_web():
    """View all enrollments"""
    enrollments = get_all_enrollments()
    return render_template('enrollments.html', enrollments=enrollments)

@app.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student_web():
    """Enroll a student"""
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        grade = request.form['grade']
        
        result = enroll_student(student_id, course_id, grade)
        if result['success']:
            flash('Student enrolled successfully!', 'success')
        else:
            flash('Error enrolling student!', 'error')
        return redirect(url_for('view_enrollments_web'))
    
    students = get_all_students()
    courses = get_all_courses()
    return render_template('enroll_student.html', students=students, courses=courses)

@app.route('/update_grade/<int:enrollment_id>', methods=['GET', 'POST'])
def update_grade_web(enrollment_id):
    """Update a student's grade"""
    if request.method == 'POST':
        grade = request.form['grade']
        result = update_grade(enrollment_id, grade)
        if result['success']:
            flash('Grade updated successfully!', 'success')
        else:
            flash('Error updating grade!', 'error')
        return redirect(url_for('view_enrollments_web'))
    
    # Get enrollment details
    enrollments = get_all_enrollments()
    enrollment = next((e for e in enrollments if e['enrollment_id'] == enrollment_id), None)
    return render_template('update_grade.html', enrollment=enrollment)

# Date Filter Routes (DEMONSTRATES DATE/TIME FILTERING)
@app.route('/filter')
def filter_page():
    """Date filter page"""
    return render_template('filter.html')

@app.route('/filter_students_by_date', methods=['POST'])
def filter_students_by_date_web():
    """Filter students by enrollment date range"""
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    students = filter_students_by_date_range(start_date, end_date)
    
    return render_template('filter_results.html', 
                         results=students, 
                         title=f"Students Enrolled from {start_date} to {end_date}",
                         type='students',
                         start_date=start_date,
                         end_date=end_date)

@app.route('/filter_enrollments_by_date', methods=['POST'])
def filter_enrollments_by_date_web():
    """Filter enrollments by date range"""
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    enrollments = filter_enrollments_by_date_range(start_date, end_date)
    
    return render_template('filter_results.html', 
                         results=enrollments, 
                         title=f"Enrollments from {start_date} to {end_date}",
                         type='enrollments',
                         start_date=start_date,
                         end_date=end_date)

@app.route('/recent_enrollments')
def recent_enrollments_web():
    """View recent enrollments (last 7 days)"""
    enrollments = get_recent_enrollments()
    
    return render_template('filter_results.html', 
                         results=enrollments, 
                         title="Recent Enrollments (Last 7 Days)",
                         type='enrollments')

@app.route('/students_by_birth_month', methods=['POST'])
def students_by_birth_month_web():
    """Filter students by birth month"""
    month = request.form['month']
    
    students = get_students_by_birth_month(month)
    
    return render_template('filter_results.html', 
                         results=students, 
                         title=f"Students Born in Month {month}",
                         type='students')

# ===================================================
# JOIN DEMONSTRATION WEB ROUTES
# ===================================================

@app.route('/joins')
def joins_page():
    """Web page for JOIN demonstrations"""
    return render_template('joins.html')

@app.route('/joins/students-with-professors')
def joins_students_with_professors():
    students = get_students_with_professors()
    return render_template('join_results.html', 
                         results=students,
                         title="Students with Their Academic Advisors",
                         join_type="INNER JOIN: students → advising → professors → departments",
                         headers=["Student ID", "Student Name", "Major", "Professor", "Department", "Status"])

@app.route('/joins/courses-with-professors')
def joins_courses_with_professors():
    courses = get_courses_with_professors()
    return render_template('join_results.html',
                         results=courses,
                         title="Courses with Assigned Professors",
                         join_type="LEFT JOIN: courses → course_assignments → professors",
                         headers=["Course ID", "Course Name", "Professor", "Semester", "Department"])

@app.route('/joins/department-statistics')
def joins_department_statistics():
    stats = get_department_statistics()
    return render_template('join_results.html',
                         results=stats,
                         title="Department Statistics",
                         join_type="Complex JOIN with Aggregation",
                         headers=["Department", "Professors", "Students", "Courses", "Avg Salary", "Avg Grade"])

# ===================================================
# API ROUTES (JSON responses for programmatic access)
# ===================================================

@app.route('/api/students', methods=['GET'])
def api_get_all_students():
    """API: Get all students"""
    students = get_all_students()
    return jsonify({
        "success": True,
        "count": len(students),
        "data": students
    })

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    """API: Get specific student"""
    student = get_student_by_id(student_id)
    if student:
        return jsonify({
            "success": True,
            "data": student
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

@app.route('/api/students', methods=['POST'])
def api_add_student():
    """API: Add new student"""
    data = request.json
    result = add_student(
        data.get('name'),
        data.get('major'),
        data.get('enrollment_date'),
        data.get('birth_date')
    )
    return jsonify(result), 201 if result['success'] else 400

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    """API: Update student"""
    data = request.json
    result = update_student(
        student_id,
        data.get('name'),
        data.get('major'),
        data.get('enrollment_date'),
        data.get('birth_date')
    )
    return jsonify(result), 200 if result['success'] else 404

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    """API: Delete student"""
    result = delete_student(student_id)
    return jsonify(result), 200 if result['success'] else 404

@app.route('/api/courses', methods=['GET'])
def api_get_all_courses():
    """API: Get all courses"""
    courses = get_all_courses()
    return jsonify({
        "success": True,
        "count": len(courses),
        "data": courses
    })

@app.route('/api/enrollments', methods=['GET'])
def api_get_all_enrollments():
    """API: Get all enrollments"""
    enrollments = get_all_enrollments()
    return jsonify({
        "success": True,
        "count": len(enrollments),
        "data": enrollments
    })

# Date Filtering API Endpoints
@app.route('/api/filter/students-by-date', methods=['GET'])
def api_filter_students_by_date():
    """API: Filter students by date range"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    students = filter_students_by_date_range(start_date, end_date)
    
    return jsonify({
        "success": True,
        "filter_type": "DATE range filter using BETWEEN",
        "count": len(students),
        "data": students
    })

@app.route('/api/filter/recent-enrollments', methods=['GET'])
def api_recent_enrollments():
    """API: Get recent enrollments"""
    enrollments = get_recent_enrollments()
    return jsonify({
        "success": True,
        "filter_type": "Relative date filter - Last 7 days",
        "count": len(enrollments),
        "data": enrollments
    })

@app.route('/api/filter/students-by-birth-month', methods=['GET'])
def api_students_by_birth_month():
    """API: Filter students by birth month"""
    month = request.args.get('month')
    students = get_students_by_birth_month(month)
    return jsonify({
        "success": True,
        "filter_type": "Date extraction using strftime()",
        "month": month,
        "count": len(students),
        "data": students
    })

# JOIN API Endpoints
@app.route('/api/joins/students-with-professors', methods=['GET'])
def api_students_with_professors():
    """API: Students with their advisors"""
    results = get_students_with_professors()
    return jsonify({
        "success": True,
        "description": "INNER JOIN across 4 tables",
        "count": len(results),
        "data": results
    })

@app.route('/api/joins/courses-with-professors', methods=['GET'])
def api_courses_with_professors():
    """API: Courses with professors"""
    results = get_courses_with_professors()
    return jsonify({
        "success": True,
        "description": "LEFT JOIN across 3 tables",
        "count": len(results),
        "data": results
    })

@app.route('/api/joins/department-statistics', methods=['GET'])
def api_department_statistics():
    """API: Department statistics"""
    results = get_department_statistics()
    return jsonify({
        "success": True,
        "description": "Complex JOIN with aggregation",
        "count": len(results),
        "data": results
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information"""
    return jsonify({
        "name": "Student Records Management System API",
        "version": "2.0.0",
        "endpoints": {
            "students": "/api/students",
            "courses": "/api/courses",
            "enrollments": "/api/enrollments",
            "date_filters": "/api/filter/...",
            "joins": "/api/joins/..."
        }
    })

# ===================================================
# RUN THE APPLICATION
# ===================================================

if __name__ == '__main__':
    print("=" * 60)
    print("   STUDENT RECORDS MANAGEMENT SYSTEM")
    print("   CSE 310 – Applied Programming")
    print("=" * 60)
    
    # Initialize database
    init_db()
    insert_sample_data()
    
    print("\n🚀 Starting Web Server...")
    print("📍 Web Interface: http://localhost:5000")
    print("📍 API Endpoints: http://localhost:5000/api/students")
    print("\n🔍 JOIN Demonstrations:")
    print("   • Web: http://localhost:5000/joins")
    print("   • API: http://localhost:5000/api/joins/students-with-professors")
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)