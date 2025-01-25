# Build 
docker-compose up --build                                               

This will:

*   Build the Flask API and PostgreSQL containers.
*   Run the API on http://localhost:5000.
*   Set up the PostgreSQL database on port 5432.

# Database Migration
*   initial migration repository
docker-compose exec backend flask db init                               
*    Generates migration scripts based on model changes
docker-compose exec backend flask db migrate -m "Initial migration"     
*    Applies the migrations to the database  
docker-compose exec backend flask db upgrade                            

# Access the API
/products	    GET	        Retrieve all products
/products	    POST	    Add a new product
/orders	        POST	    Place a new order
/orders	        GET	        Retrieve all orders
/invalid_url    GET/POST    Invalid Route Response

# Test Coverage

*   Successful and edge cases for all API endpoints.
*   Stock validation during order placement.
*   Error handling for invalid requests.