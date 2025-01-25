from flask import Blueprint, request, jsonify
from models.order import Order
from models.product import Product
from models import db

bp = Blueprint('order_routes', __name__, url_prefix='/orders')

@bp.route('/', methods=['POST'])
def place_order():
   
    data = request.json         # Get the JSON data from the request body

    # Validation    
    if not data:                # Check if the request body is missing
        return jsonify({"error": "Request body is missing."}), 400

    # Check if the 'products' field is missing or not a list or empty
    if 'products' not in data or not isinstance(data['products'], list) or len(data['products']) == 0:
        return jsonify({"error": "'products' must be a non-empty list."}), 400

    total_price = 0
    updated_stock = {}

    try:
        for item in data['products']:
            # Check if each product has 'product_id' and 'quantity'
            if 'product_id' not in item or 'quantity' not in item:  
                return jsonify({"error": "Each product must have 'product_id' and 'quantity'."}), 400

            # Check if 'product_id' and 'quantity' are integers
            if not isinstance(item['product_id'], int) or not isinstance(item['quantity'], int):
                return jsonify({"error": "'product_id' and 'quantity' must be integers."}), 400

            # Check if 'quantity' is greater than 0
            if item['quantity'] <= 0:
                return jsonify({"error": "'quantity' must be greater than zero."}), 400

            # Check if the product exists
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({"error": f"Product ID {item['product_id']} does not exist."}), 404

            # Check if there is enough stock
            if product.stock < item['quantity']:
                return jsonify({"error": f"Insufficient stock for product ID {item['product_id']}."}), 400

            # Calculate total price
            total_price += product.price * item['quantity']
            # Update stock
            updated_stock[product.id] = product.stock - item['quantity']

        # Deduct stock and create the order
        for product_id, new_stock in updated_stock.items(): #key is product_id and value is new_stock
            product = Product.query.get(product_id)
            product.stock = new_stock

        new_order = Order(products=data['products'], total_price=total_price)
        db.session.add(new_order)
        db.session.commit()

        return jsonify({"message": "Order placed successfully!", "order_id": new_order.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/', methods=['GET'])
def get_all_orders():
    try:
        orders = Order.query.all()
        result = [order.to_dict() for order in orders]      # Convert each order to dictionary
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500