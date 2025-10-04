import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize the Flask application
app = Flask(__name__)

# Set up configuration for SQLAlchemy and secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'mysecretkey'

# Configure the upload folder for file uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'} #'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS


# Define a custom base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the custom base class
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Set up Flask-Migrate for database migrations
Migrate(app, db)

# Initialize Flask-Login for user session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to 'login' view if not authenticated
login_manager.login_message = "Please log in to access this page!"  # Message for login required