import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add the parent directory to PYTHONPATH
from app import create_app
from models import db

@pytest.fixture
def client():
    # Choose your environment: 'testing' or 'production'
    app = create_app("testing")  # Change to 'production' for production config
    app.config["TESTING"] = True  # Ensure you're in testing mode

    with app.test_client() as client:
        with app.app_context():
            # upgrade()  # Apply migrations (replaces db.create_all())
            pass
        yield client  # Provide the test client
        with app.app_context():
            # db.drop_all()  # Clean up after tests
            pass
