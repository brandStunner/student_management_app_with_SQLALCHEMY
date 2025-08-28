import os
import psycopg2
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

load_dotenv()
app = Flask(__name__)

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# CREATING A DATABASE URI (Fixed syntax)
password_used = quote_plus(DB_PASSWORD)
DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{password_used}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# initialize the database
db = SQLAlchemy(app)

# create table(using a class instead of sql scripts)
class StudentManagementSystem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
   

    def __repr__(self):
        return f"<Student {self.name}>"

with app.app_context():
    db.create_all()
@app.route("/")
def welcome_page():
    return jsonify({"message": "Welcome to our main page"})


@app.route("/home", methods= ["GET"])
def home():
    try:
        # Get all students from the database
        students = StudentManagementSystem.query.all()

        # Convert to serializable format
        students_data = []
        for student in students:
            students_data.append({
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "email": student.email
            })

        return jsonify({
            "message": "Welcome to the homepage - All Students",
            "total_students": len(students_data),
            "students": students_data
        })
    except Exception as e:
        return jsonify({"Error": "Failed to retrieve students", "error": str(e)}), 500
       

        

@app.route("/students", methods=["POST"])
def create_student():
    try:
        data = request.get_json()
        name = data.get("name")
        age = data.get("age")
        email = data.get("email")
        
        if not name or not age or not email:
            return jsonify({"error": "Missing fields. name, age, email must be provided"}),400
        
        new_student = StudentManagementSystem(name=name, age = age, email = email)
        db.session.add(new_student)
        db.session.commit()

        student_data = {
            "id": new_student.id,
            "name": new_student.name,
            "age": new_student.age,
            "email": new_student.email
        }
        return make_response(jsonify({"message": "data created", "data": student_data}),200)
    
            
        
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"Error": "Student with this email already exists"}), 409)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"Error": "error creating student", "error": str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=True)
