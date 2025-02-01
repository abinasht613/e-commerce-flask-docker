from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, init_db
from routes import product_routes, order_routes
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Access environment variables
DB_NAME     = os.getenv("POSTGRES_DB")
DB_USER     = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST     = os.getenv("POSTGRES_HOST", "db")  # Default host is 'db' (service name in Docker Compose)
DB_PORT     = os.getenv("POSTGRES_PORT", "5432")  # Default port is 5432
FLASK_ENV     = os.getenv("FLASK_ENV")

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)      # Run the app


def create_app(config_name="production"):
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Set the configuration for the app based on the passed environment
    if config_name == "testing":
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif config_name == "production":
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Initialize CORS, Database, and other app-level components
    CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})  # Enable CORS
    
    # Initialize the database and migration engine
    init_db(app)
    Migrate(app, db)

    # Register blueprints for the routes
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(order_routes.bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Route not found: 404"})

    return app