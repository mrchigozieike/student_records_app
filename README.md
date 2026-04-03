# SQL Database API Project

## Overview
This project is a simple REST API built using Python and Flask that interacts with a SQLite relational database.

The API allows users to:
- View students stored in a database
- Add new students

## Technologies Used
- Python
- Flask
- SQLite
- REST API

## Project Structure
SQL_Database_Project
api.py
database.py
students.db
requirements.txt
README.md

## How to Run Locally

Install dependencies

pip install -r requirements.txt

Run the API

python api.py

The API will start at:
http://127.0.0.1:5000

## API Endpoints

GET /students  
Returns a list of all students.

POST /students  
Adds a new student.

Example JSON body:

{
"name": "Alice",
"age": 22,
"major": "Software Development"
}

## Deployment
This project can be deployed online using Render or other Python hosting platforms.