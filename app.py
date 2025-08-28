import os
import psycopg2
from flask import Flask, jsonify, request
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




# Test connection
# try:
#     engine = create_engine(DATABASE_URI)
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))
#         print("✅ Database connection successful!")
#         print(f"Test result: {result.fetchone()}")
# except Exception as e:
#     print(f"❌ Database connection failed: {e}")