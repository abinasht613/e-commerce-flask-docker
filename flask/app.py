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

# Initialize Flask app
# Create a Flask app
app = Flask(__name__)   
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})  # Enable CORS    
# Set the database URL
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Disable modification tracking                    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize the database
init_db(app) 
migrate = Migrate(app, db)  #   Initialize the migration engine

# Register blueprints
app.register_blueprint(product_routes.bp)
app.register_blueprint(order_routes.bp)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"message": "Route not found:404"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)      # Run the app
