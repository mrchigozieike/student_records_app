from flask import Flask, request
from flask_restx import Api, Resource, fields
import database

app = Flask(__name__)

# Swagger API initialization
api = Api(
    app,
    version='1.0',
    title='Student Database API',
    description='API for managing student records using SQLite'
)

ns = api.namespace('students', description='Student operations')

# Create database table when server starts
database.create_table()


# -----------------------
# Swagger Data Model
# -----------------------
student_model = api.model('Student', {
    'name': fields.String(required=True, description='Student name'),
    'age': fields.Integer(required=True, description='Student age'),
    'major': fields.String(required=True, description='Student major')
})


# -----------------------
# GET all students
# -----------------------
@ns.route('/')
class StudentList(Resource):

    @ns.doc('list_students')
    def get(self):
        """Retrieve all students"""
        return database.get_students()

    @ns.expect(student_model)
    @ns.doc('create_student')
    def post(self):
        """Add a new student"""

        data = request.json
        database.insert_student(
            data['name'],
            data['age'],
            data['major']
        )

        return {"message": "Student added successfully"}, 201


# -----------------------
# Update / Delete student
# -----------------------
@ns.route('/<int:id>')
class Student(Resource):

    @ns.expect(student_model)
    @ns.doc('update_student')
    def put(self, id):
        """Update a student"""

        data = request.json
        database.update_student(
            id,
            data['name'],
            data['age'],
            data['major']
        )

        return {"message": "Student updated"}

    @ns.doc('delete_student')
    def delete(self, id):
        """Delete a student"""

        database.delete_student(id)

        return {"message": "Student deleted"}


# -----------------------
# Aggregate Statistics
# -----------------------
@ns.route('/stats')
class StudentStats(Resource):

    @ns.doc('student_statistics')
    def get(self):
        """Return total students and average age"""

        return database.get_student_statistics()


if __name__ == "__main__":
    app.run(debug=True)