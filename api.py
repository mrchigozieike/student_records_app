# Import the Flask framework used to create the web API
from flask import Flask, jsonify, request

# Import functions from database.py to interact with the database
from database import get_students, add_student

# Create the Flask application instance
app = Flask(__name__)

# -----------------------------
# ROUTE: Home
# -----------------------------
# This route runs when someone visits the base URL of the API
# Example: https://your-api-url.onrender.com/
@app.route("/")
def home():
    return jsonify({"message": "Student API is running"})


# -----------------------------
# ROUTE: Get all students
# -----------------------------
# This route retrieves all student records from the database
# Example request:
# GET /students
@app.route("/students", methods=["GET"])
def students():
    
    # Call function from database.py to retrieve student data
    students = get_students()
    
    # Return the students as JSON
    return jsonify(students)


# -----------------------------
# ROUTE: Add a new student
# -----------------------------
# This route allows users to add a student to the database
# Example request:
# POST /students
# JSON body:
# {
#   "name": "John Doe",
#   "age": 21,
#   "major": "Computer Science"
# }
@app.route("/students", methods=["POST"])
def add():

    # Get JSON data sent in the request body
    data = request.json

    # Extract fields from the request
    name = data.get("name")
    age = data.get("age")
    major = data.get("major")

    # Add the student to the database
    add_student(name, age, major)

    # Return confirmation message
    return jsonify({"message": "Student added successfully"})


# -----------------------------
# Run the Flask server
# -----------------------------
# This runs the application locally when executing api.py
# Debug mode allows automatic reload when code changes
if __name__ == "__main__":
    app.run(debug=True)