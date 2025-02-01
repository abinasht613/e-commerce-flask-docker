from flask import Blueprint, request, jsonify
from models.order import Order
from models.product import Product
from models import db

from validations.schema import OrderSchema

order_schema = OrderSchema()

bp = Blueprint('order_routes', __name__, url_prefix='/orders')

@bp.route('/', methods=['POST'])
def place_order():
    try:
        data    = request.get_json()
        errors  = order_schema.validate(data,session=db.session)
    
        if errors:
            return jsonify(errors), 400
        # Initialize variables for price calculation and stock updates
        total_price = 0
        updated_stock = {}

        # Get all product IDs from the order at once
        product_ids = [item['product_id'] for item in data['products']]
        
        # Query products in bulk (minimize number of queries)
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        products_map = {product.id: product for product in products}  # Map product_id to product object

        # Check stock availability and calculate total price
        for item in data['products']:
            product = products_map.get(item['product_id'])
            
            if not product:
                return jsonify({"error": f"Product ID {item['product_id']} not found."}), 400

            # Lock the product row for updating its stock (this prevents race conditions)
            product = Product.query.filter(Product.id == item['product_id']).with_for_update().first()

            if product.stock < item['quantity']:
                return jsonify({"error": f"Insufficient stock for product ID {item['product_id']}."}), 400
            
            # Calculate total price and update stock information
            total_price += product.price * item['quantity']
            updated_stock[product.id] = product.stock - item['quantity']

        try:
            # Update stock and create order without manually handling the transaction
            # SQLAlchemy automatically starts a transaction on the first query or update
            for product_id, new_stock in updated_stock.items():
                product = products_map.get(product_id)
                product.stock = new_stock  # Update the stock quantity

            # Prepare the new order data
            new_order = order_schema.load({"products": data['products'], "total_price": total_price}, session=db.session)

            # Add new order to the session
            db.session.add(new_order)

            # Commit the transaction
            db.session.commit()

            return jsonify({"message": "Order placed successfully!"}), 201

        except Exception as e:
            # In case of error, we rollback the transaction
            db.session.rollback()  # Rollback changes if any error occurs
            return jsonify({"error": f"An error occurred while placing the order: {str(e)}"}), 500
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