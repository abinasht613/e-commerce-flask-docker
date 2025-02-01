def test_place_order(client):
    """Test placing an order successfully."""
    # Add a product first
    client.post("/products/", json={"name": "Phone", "description": "Smartphone", "price": 800, "stock": 5})

    order_data = {
        "products": [
            {"product_id": 1, "quantity": 2}
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    assert response.json["message"] == "Order placed successfully!"

def test_insufficient_stock(client):
    """Test order placement with insufficient stock."""
    client.post("/products/", json={"name": "Headphones", "description": "Wireless", "price": 100, "stock": 1})

    order_data = {
        "products": [
            {"product_id": 1, "quantity": 100}  # More than available stock
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 400
    assert "Insufficient stock" in response.json["error"]

def test_get_orders(client):
    """Test retrieving all orders."""
    response = client.get("/orders/")
    assert response.status_code == 200
