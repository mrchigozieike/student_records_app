# api.py
# Flask API for managing student records using SQLite

from flask import Flask, request, jsonify
from flasgger import Swagger
from database import get_db_connection, init_db

app = Flask(__name__)

# Enable Swagger Documentation
swagger = Swagger(app)

# Initialize database tables
init_db()


@app.route("/")
def home():
    """
    API Home
    ---
    responses:
      200:
        description: API is running
    """
    return {"message": "Student Records API Running"}


# ------------------------------
# GET ALL STUDENTS
# ------------------------------
@app.route("/students", methods=["GET"])
def get_students():
    """
    Get all students
    ---
    responses:
      200:
        description: List of students
    """
    try:

        conn = get_db_connection()
        students = conn.execute("SELECT * FROM students").fetchall()
        conn.close()

        return jsonify([dict(student) for student in students])

    except Exception as e:
        return {"error": str(e)}, 500


# ------------------------------
# ADD STUDENT
# ------------------------------
@app.route("/students", methods=["POST"])
def add_student():
    """
    Add a new student
    ---
    parameters:
      - name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            age:
              type: integer
            department_id:
              type: integer
    responses:
      201:
        description: Student added
    """

    try:

        data = request.get_json()

        name = data["name"]
        age = data["age"]
        department_id = data["department_id"]

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO students (name, age, department_id) VALUES (?, ?, ?)",
            (name, age, department_id),
        )

        conn.commit()
        conn.close()

        return {"message": "Student added successfully"}, 201

    except Exception as e:
        return {"error": str(e)}, 500


# ------------------------------
# UPDATE STUDENT
# ------------------------------
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    """
    Update a student
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    """

    try:

        data = request.get_json()

        name = data["name"]
        age = data["age"]

        conn = get_db_connection()

        conn.execute(
            "UPDATE students SET name = ?, age = ? WHERE id = ?",
            (name, age, id),
        )

        conn.commit()
        conn.close()

        return {"message": "Student updated successfully"}

    except Exception as e:
        return {"error": str(e)}, 500


# ------------------------------
# DELETE STUDENT
# ------------------------------
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    """
    Delete a student
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    """

    try:

        conn = get_db_connection()

        conn.execute("DELETE FROM students WHERE id = ?", (id,))

        conn.commit()
        conn.close()

        return {"message": "Student deleted"}

    except Exception as e:
        return {"error": str(e)}, 500


# ------------------------------
# JOIN QUERY (ADVANCED SQL)
# ------------------------------
@app.route("/students-with-department", methods=["GET"])
def students_with_department():
    """
    Get students with department names (JOIN)
    ---
    responses:
      200:
        description: Students with departments
    """

    try:

        conn = get_db_connection()

        students = conn.execute(
            """
            SELECT students.id,
                   students.name,
                   students.age,
                   departments.name AS department
            FROM students
            JOIN departments
            ON students.department_id = departments.id
            """
        ).fetchall()

        conn.close()

        return jsonify([dict(student) for student in students])

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True)