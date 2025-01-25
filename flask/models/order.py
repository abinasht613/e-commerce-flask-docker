from sqlalchemy.dialects.postgresql import JSON
from . import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.Column(JSON, nullable=False)               # JSON for easier storage of product lists
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)

    def to_dict(self):                      # Convert the order to a dictionary
        return {
            "id": self.id,                  
            "products": self.products,      # JSON is serializable
            "total_price": self.total_price,
            "status": self.status
        }
