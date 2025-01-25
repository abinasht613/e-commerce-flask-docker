from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()           # Create a SQLAlchemy instance

def init_db(app):           # Initialize the database with the Flask app
    db.init_app(app)        # Initialize the SQLAlchemy app
