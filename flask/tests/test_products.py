def test_get_products(client):
    """Test retrieving all products (empty initially)."""
    response = client.get("/products/")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    if 'Location' in response.headers:
        print(f"Redirected to: {response.headers['Location']}")
    assert response.status_code == 200
    # Check if the response JSON is an empty list or contains products
    if response.json == []:
        print("No products found.")
    else:
        print("Products found:", response.json)

    # Assert the response JSON is either empty or contains a list of products
    assert isinstance(response.json, list)  # Ensure it's a list (could be empty or have products)

def test_add_product(client):
    """Test adding a new product."""
    new_product = {
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 1500.0,
        "stock": 10
    }
    response = client.post("/products/", json=new_product)
    assert response.status_code == 201
    assert response.json["message"] == "Product added successfully!"

def test_add_product_invalid(client):
    """Test adding a product with missing fields."""
    response = client.post("/products/", json={"name": "Tablet"})
    assert response.status_code == 400  # Bad Request
