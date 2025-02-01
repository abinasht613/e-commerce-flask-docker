from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validates, ValidationError, fields
from models.product import Product
from models.order import Order


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True  # Load SQLAlchemy instances instead of dictionaries

    id          = auto_field(dump_only=True)
    name        = auto_field(required=True)
    description = auto_field(required=True)
    price       = auto_field(required=True)
    stock       = auto_field(required=True)

    @validates("price")
    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be greater than zero.")

    @validates("stock")
    def validate_stock(self, value):
        if value < 0:
            raise ValidationError("Stock must be a non-negative integer.")

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        # exclude = ('total_price', 'status')

    id          = auto_field(dump_only=True)
    products    = fields.List(fields.Dict(keys=fields.Str(), values=fields.Int()), required=True)
    total_price = fields.Float(allow_none=True)  # Optional field, allows None
    status      = fields.Str(allow_none=True)  # Optional field, allows None

    @validates("products")
    def validate_products(self, value):
        try:
            if not value:
                raise ValidationError("At least one product is required.")
            for item in value:
                if "product_id" not in item or "quantity" not in item:
                    raise ValidationError("Each item must have 'product_id' and 'quantity'.")
                
                # Validate 'product_id' as a positive integer
                try:
                    product_id = int(item["product_id"])  # Convert to integer
                    if product_id <= 0:
                        raise ValidationError(f"Product ID must be a positive integer. Provided: {product_id}")
                except ValueError:
                    raise ValidationError(f"Product ID must be a valid integer. Provided: {item['product_id']}")

                # Validate 'quantity' as a positive integer
                try:
                    quantity = int(item["quantity"])  # Convert to integer
                    if quantity <= 0:
                        raise ValidationError(f"Quantity must be a positive integer. Provided: {quantity}")
                except ValueError:
                    raise ValidationError(f"Quantity must be a valid integer. Provided: {item['quantity']}")

                # Check if product_id exists in the database (validation step)
                product_id = item["product_id"]
                product = Product.query.get(product_id)  # Assuming you're using SQLAlchemy
                if not product:
                    raise ValidationError(f"Product with ID {product_id} does not exist.")
                
                if item["quantity"] <= 0:
                    raise ValidationError("Quantity must be greater than zero.")
        except Exception as e:
            raise ValidationError(str(e))
        