## SQL Relational Database API
Author Chigozie Henry Ike
CSE 310 – Applied Programming

## Project Purpose

The purpose of this project is to demonstrate how a software application can interact with a relational database using SQL. The project shows how a backend API can perform CRUD operations (Create, Read, Update, Delete) while maintaining structured data inside a relational database.

This project was created as part of CSE 310 – Applied Programming to demonstrate:

Database connectivity
SQL queries and relational data management
API development using Python
Error handling and validation
Documentation using Swagger (OpenAPI)

The application simulates a student records management system where users can add, update, view, and delete student records.

## Project Overview

This project is a Student Database API built using Python, Flask, and SQLite. The API allows users to interact with a relational database through HTTP requests.

The system stores student information such as:

Student Name
Age
Major

The API supports the following features:

Add new students to the database
Retrieve all students
Retrieve a specific student by ID
Update student information
Delete student records
Generate aggregate statistics such as average age
Interactive API testing using Swagger documentation

This project demonstrates how relational databases work with backend applications and how APIs allow different systems to communicate with a database.

## Time Log (Time Spent)
Task                            	Time Spent
Project planning and research	    2 hour
Creating database schema	        3 hour
Writing database connection code	3 h0urs
Developing CRUD API endpoints	    2 hours
Implementing error handling	        2 hour
Adding Swagger API documentation	1 hour
Testing API endpoints	            2 hours 
Deployment to Render	            2 hours 
Writing README documentation	    3 hour

Total Time Spent: 20 hours

## Technologies Used
Python
Flask
SQLite
SQL
Flask-RESTX (Swagger Documentation)
Gunicorn
Render (Cloud Deployment)
Development Environment

## This project was developed using the following tools:

Visual Studio Code
Python 3.x
SQLite Database
Git
GitHub
Postman / Browser for API testing

The application was tested locally and deployed online using Render.

Project Structure
student_records_app
│
├── api.py
├── database.py
├── students.db
├── requirements.txt
└── README.md

File descriptions

api.py
Contains the Flask API routes and handles HTTP requests such as GET, POST, PUT, and DELETE.

database.py
Handles the database connection and SQL queries.

students.db
SQLite relational database that stores student records.

requirements.txt
Lists the required Python packages needed to run the project.

README.md
Contains documentation explaining the project.

API Endpoints
Method	Endpoint	Description
GET	/students	Retrieve all students
GET	/students/<id>	Retrieve a specific student
POST	/students	Add a new student
PUT	/students/<id>	Update student information
DELETE	/students/<id>	Delete a student
GET	/students/stats	View student statistics
How to Run the Program (Offline)
1️⃣ Install Python

Make sure Python 3 is installed.

Check with:

python --version
2️⃣ Install required packages
pip install -r requirements.txt
3️⃣ Start the application

Run:

python api.py
4️⃣ Open the API in your browser
http://127.0.0.1:5000

Swagger documentation will appear where you can test all endpoints.

How to Run the Program (Online)

This API is deployed online using Render.

You can access the API using the deployed URL:

https://sql-database-api.onrender.com



You can test API endpoints directly from the browser using the Swagger documentation interface.

http://127.0.0.1:5000/apidocs/#/

Example endpoint:

https://sql-database-api.onrender.com


Example JSON Request

To add a student:

POST /students

Example request body:

{
  "name": "Alice Johnson",
  "age": 22,
  "major": "Software Development"
}

Example response:

{
  "message": "Student added successfully"
}
API Documentation

This project includes Swagger (OpenAPI) documentation using Flask-RESTX.

Swagger provides an interactive interface where users can:

View all API endpoints
Read endpoint descriptions
Send test requests directly from the browser
View response data

Swagger documentation is available at:

/docs

Example:

https://sql-database-api.onrender.com/docs
Learning Outcomes

Through this project I learned:

How relational databases work
Writing SQL queries
Building REST APIs using Flask
Connecting Python applications to databases
Handling errors in backend applications
Creating professional API documentation
Deploying applications online
Future Improvements

Possible improvements for the project include:

Adding authentication and user accounts
Using PostgreSQL instead of SQLite
Adding pagination for large datasets
Creating a frontend interface for the API
Improving validation and security