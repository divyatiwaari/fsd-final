"""
Unit tests for the Items API backend using pytest.

This test suite covers:
- GET /items endpoint
- POST /items endpoint
- GET /items/{id} endpoint
- PUT /items/{id} endpoint
- DELETE /items/{id} endpoint
- Edge cases and error handling
"""

import pytest
from fastapi.testclient import TestClient
from main import app, items_db, reset_db

# Create a test client
client = TestClient(app)

# ============= Fixtures =============

@pytest.fixture(autouse=True)
def reset_database():
    """
    Reset the in-memory database before each test.
    This ensures tests don't interfere with each other.
    """
    reset_db()
    yield
    reset_db()

# ============= Test Health Check =============

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# ============= Test GET /items =============

def test_get_items_empty():
    """Test retrieving items when the list is empty"""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []

def test_get_items_with_pagination():
    """Test retrieving items with skip and limit parameters"""
    # Create 5 items
    for i in range(5):
        client.post("/items", json={"name": f"Item {i}"})
    
    # Test skip and limit
    response = client.get("/items?skip=1&limit=2")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["name"] == "Item 1"
    assert items[1]["name"] == "Item 2"

def test_get_items_multiple():
    """Test retrieving multiple items"""
    # Create items
    names = ["Apple", "Banana", "Orange"]
    for name in names:
        client.post("/items", json={"name": name})
    
    # Get all items
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3
    assert items[0]["name"] == "Apple"
    assert items[1]["name"] == "Banana"
    assert items[2]["name"] == "Orange"

# ============= Test POST /items =============

def test_create_item_success():
    """Test creating a new item successfully"""
    response = client.post("/items", json={"name": "Test Item", "description": "A test item"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert data["id"] is not None
    assert isinstance(data["id"], int)

def test_create_item_without_description():
    """Test creating an item without a description"""
    response = client.post("/items", json={"name": "Simple Item"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Simple Item"
    assert data["description"] is None
    assert data["id"] is not None

def test_create_item_empty_name():
    """Test creating an item with an empty name (should fail)"""
    response = client.post("/items", json={"name": ""})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]

def test_create_item_whitespace_name():
    """Test creating an item with only whitespace as name (should fail)"""
    response = client.post("/items", json={"name": "   "})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]

def test_create_item_name_stripped():
    """Test that item names are trimmed of whitespace"""
    response = client.post("/items", json={"name": "  Trimmed Item  "})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Trimmed Item"

def test_create_multiple_items_unique_ids():
    """Test that created items have unique IDs"""
    response1 = client.post("/items", json={"name": "Item 1"})
    response2 = client.post("/items", json={"name": "Item 2"})
    
    id1 = response1.json()["id"]
    id2 = response2.json()["id"]
    
    assert id1 != id2
    assert id1 < id2  # IDs should increment

# ============= Test GET /items/{id} =============

def test_get_item_success():
    """Test retrieving a specific item by ID"""
    # Create an item
    create_response = client.post("/items", json={"name": "Test Item"})
    item_id = create_response.json()["id"]
    
    # Get the item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Test Item"

def test_get_item_not_found():
    """Test retrieving a non-existent item (should return 404)"""
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_get_item_after_creation():
    """Test that created item can be retrieved"""
    created = client.post("/items", json={"name": "New Item", "description": "Test description"})
    item_id = created.json()["id"]
    
    retrieved = client.get(f"/items/{item_id}")
    assert retrieved.status_code == 200
    assert retrieved.json() == created.json()

# ============= Test PUT /items/{id} =============

def test_update_item_name():
    """Test updating an item's name"""
    # Create an item
    create_response = client.post("/items", json={"name": "Original"})
    item_id = create_response.json()["id"]
    
    # Update the item
    update_response = client.put(f"/items/{item_id}", json={"name": "Updated"})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated"
    assert data["id"] == item_id

def test_update_item_description():
    """Test updating an item's description"""
    # Create an item
    create_response = client.post("/items", json={"name": "Item"})
    item_id = create_response.json()["id"]
    
    # Update description
    update_response = client.put(f"/items/{item_id}", json={"description": "New description"})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["description"] == "New description"
    assert data["name"] == "Item"

def test_update_item_not_found():
    """Test updating a non-existent item (should return 404)"""
    response = client.put("/items/9999", json={"name": "Updated"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_item_empty_name():
    """Test updating item with empty name (should fail)"""
    # Create an item
    create_response = client.post("/items", json={"name": "Original"})
    item_id = create_response.json()["id"]
    
    # Try to update with empty name
    update_response = client.put(f"/items/{item_id}", json={"name": ""})
    assert update_response.status_code == 400
    assert "cannot be empty" in update_response.json()["detail"]

def test_update_item_partial():
    """Test partial update (only updating one field)"""
    # Create an item
    create_response = client.post("/items", json={"name": "Item", "description": "Desc"})
    item_id = create_response.json()["id"]
    
    # Update only name
    update_response = client.put(f"/items/{item_id}", json={"name": "New Name"})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "New Name"
    assert data["description"] == "Desc"

# ============= Test DELETE /items/{id} =============

def test_delete_item_success():
    """Test deleting an item successfully"""
    # Create an item
    create_response = client.post("/items", json={"name": "To Delete"})
    item_id = create_response.json()["id"]
    
    # Delete the item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204
    
    # Verify item is deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_delete_item_not_found():
    """Test deleting a non-existent item (should return 404)"""
    response = client.delete("/items/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_delete_item_removes_from_list():
    """Test that deleted item is no longer in the list"""
    # Create two items
    item1 = client.post("/items", json={"name": "Item 1"}).json()
    item2 = client.post("/items", json={"name": "Item 2"}).json()
    
    # Delete first item
    client.delete(f"/items/{item1['id']}")
    
    # Check list only contains second item
    response = client.get("/items")
    items = response.json()
    assert len(items) == 1
    assert items[0]["id"] == item2["id"]

# ============= Test DELETE /items =============

def test_delete_all_items():
    """Test deleting all items"""
    # Create multiple items
    client.post("/items", json={"name": "Item 1"})
    client.post("/items", json={"name": "Item 2"})
    client.post("/items", json={"name": "Item 3"})
    
    # Verify items were created
    response = client.get("/items")
    assert len(response.json()) == 3
    
    # Delete all items
    delete_response = client.delete("/items")
    assert delete_response.status_code == 204
    
    # Verify all items are deleted
    response = client.get("/items")
    assert len(response.json()) == 0

def test_delete_all_items_when_empty():
    """Test deleting all items when list is already empty"""
    response = client.delete("/items")
    assert response.status_code == 204

# ============= Integration Tests =============

def test_full_workflow():
    """Test a complete workflow: create, read, update, and delete"""
    # 1. Create item
    create_response = client.post("/items", json={"name": "Workflow Item", "description": "Original"})
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # 2. Read item
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Workflow Item"
    
    # 3. Update item
    update_response = client.put(f"/items/{item_id}", json={"description": "Updated"})
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Updated"
    
    # 4. Delete item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204
    
    # 5. Verify deletion
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_multiple_operations():
    """Test multiple CRUD operations in sequence"""
    # Create multiple items
    ids = []
    for i in range(3):
        response = client.post("/items", json={"name": f"Item {i}"})
        ids.append(response.json()["id"])
    
    # Retrieve all
    response = client.get("/items")
    assert len(response.json()) == 3
    
    # Delete middle item
    client.delete(f"/items/{ids[1]}")
    
    # Verify only 2 items remain
    response = client.get("/items")
    assert len(response.json()) == 2
    
    # Update first item
    client.put(f"/items/{ids[0]}", json={"name": "Modified Item 0"})
    
    # Verify update
    response = client.get(f"/items/{ids[0]}")
    assert response.json()["name"] == "Modified Item 0"
