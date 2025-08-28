
import os
import psycopg2
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from sqlalchemy.exc import IntegrityError
load_dotenv()
app = Flask(__name__)

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


# CREATING A DATABASE URI
app.config = ["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgress"
