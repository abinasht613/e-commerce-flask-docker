from flask import Blueprint, request, jsonify
from models.product import Product
from models import db

bp = Blueprint('product_routes', __name__, url_prefix='/products')  # Create a Blueprint object

@bp.route('/', methods=['GET'])     
def get_products():                     
    products = Product.query.all()      # Get all products from the database
    result = [
        {"id": p.id, "name": p.name, "description": p.description, "price": p.price, "stock": p.stock}
        for p in products               # list comprehension
    ]
    return jsonify(result), 200

@bp.route('/', methods=['POST'])
def add_product():

    data = request.json         # Get the JSON data from the request body

    # Validation                # Check if the request body is missing
    if not data:
        return jsonify({"error": "Request body is missing."}), 400

    required_fields = ["name", "description", "price", "stock"]     # Check if the required fields are missing
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is a required field."}), 400

    if not isinstance(data['name'], (str)):                         # Check if the data types is string
        return jsonify({"error": "'name' must be a string."}), 400
    
    if not isinstance(data['description'], (str)):                  # Check if the data types is string
        return jsonify({"error": "'description' must be a string."}), 400

    if not isinstance(data['price'], (float, int)) or data['price'] <= 0:   # Check if the data types is float or int
        return jsonify({"error": "'price' must be a positive number."}), 400

    if not isinstance(data['stock'], int) or data['stock'] < 0:             # Check if the data types is int
        return jsonify({"error": "'stock' must be a non-negative integer."}), 400

    # Create and save the product
    try:
        new_product = Product(
            name        =   data['name'],
            description =   data['description'],
            price       =   float(data['price']),
            stock       =   int(data['stock'])
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully!", "product_id": new_product.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
