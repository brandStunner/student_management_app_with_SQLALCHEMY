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

@app.route("/home", methods= ["GET","POST"])
def home():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error":"no data provided"}),400
        
        name = data.get("name")
        age = data.get("age")
        email = data.get("email")
               
        return jsonify({"message": "data recieved", "data": data})
    return jsonify({"Welcome to the homepage"})

        

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

        return make_response(jsonify({"message": "data created", "data": new_student}),200)
            
    except Exception as e:
        return make_response(jsonify({"Error": "error creating student", "error":str(e)}), 500)

# print(StudentManagementSystem.__tablename__)

 










# Test connection
# try:
#     engine = create_engine(DATABASE_URI)
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))
#         print("✅ Database connection successful!")
#         print(f"Test result: {result.fetchone()}")
# except Exception as e:
#     print(f"❌ Database connection failed: {e}")