# copy .env.example to .env
# copy .env.example to .env.test

# Build Test cases in Testing Container
*   FLASK_ENV=testing in .env.test
*   docker-compose -f docker-compose-test.yaml up --build -d
*   docker-compose exec backend_test flask db init
*   docker-compose exec backend_test flask db migrate -m "Initial migration"
*   docker-compose exec backend_test flask db upgrade
*   docker-compose exec backend_test pytest -v
*   docker-compose -f docker-compose-test.yaml down -v


# Build Production Container
*   FLASK_ENV=production in .env
*   docker-compose up --build -d   
*   docker-compose exec backend flask db init                                         
*   docker-compose exec backend flask db migrate -m "Initial migration"   
*   docker-compose exec backend flask db upgrade
*   docker-compose down -v

This will:

*   Build the Flask API and PostgreSQL containers.
*   Run the API on http://localhost:5000.
*   Set up the PostgreSQL database on port 5432.

# Database Migration
*   initial migration repository:<br/> **docker-compose exec backend flask db init**                               
*    Generates migration scripts based on model changes :<br/> **docker-compose exec backend flask db migrate -m "Initial migration"**
*    Applies the migrations to the database:<br/> **docker-compose exec backend flask db upgrade**                            

# Access the API
| route        | method    | Description                |
| -------------| ----------| -------------------------- |
| /products    | GET       |    Retrieve all products   |
| /products	   | POST	   |    Add a new product       |
| /orders	   | POST	   |    Place a new order       |
| /orders	   | GET	   |    Retrieve all orders     |
| /invalid_url | GET/POST  |    Invalid Route Response  |


# Test Coverage

*   Successful and edge cases for all API endpoints.
*   Stock validation during order placement.
*   Error handling for invalid requests.