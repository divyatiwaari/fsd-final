"""
Simple FastAPI application for managing items.
This API provides endpoints to create, retrieve, and delete items.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI application
app = FastAPI(title="Items API", version="1.0.0")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= Data Models =============
class Item(BaseModel):
    """Pydantic model for Item"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    """Pydantic model for updating an item"""
    name: Optional[str] = None
    description: Optional[str] = None

# ============= In-Memory Data Store =============
# Simple in-memory list to store items
items_db: List[Item] = []
next_id = 1

# ============= Helper Functions =============
def reset_db():
    """Reset the database to initial state (useful for testing)"""
    global items_db, next_id
    items_db = []
    next_id = 1

def get_next_id() -> int:
    """Generate the next available ID"""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

def find_item(item_id: int) -> Optional[Item]:
    """Find an item by ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    return None

# ============= Routes =============

@app.get("/", tags=["root"])
def read_root():
    """Welcome endpoint"""
    return {"message": "Welcome to Items API"}

@app.get("/items", response_model=List[Item], tags=["items"])
def get_items(skip: int = 0, limit: int = 10):
    """
    Retrieve all items with optional pagination.
    
    - **skip**: Number of items to skip (default: 0)
    - **limit**: Maximum number of items to return (default: 10)
    """
    return items_db[skip : skip + limit]

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(item: Item):
    """
    Create a new item.
    
    - **name**: Name of the item (required)
    - **description**: Optional description of the item
    """
    # Validation: name should not be empty
    if not item.name or not item.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item name cannot be empty"
        )
    
    # Create new item with ID
    new_item = Item(
        id=get_next_id(),
        name=item.name.strip(),
        description=item.description
    )
    items_db.append(new_item)
    return new_item

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int):
    """
    Retrieve a specific item by ID.
    
    - **item_id**: The ID of the item to retrieve
    """
    item = find_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, item_update: ItemUpdate):
    """
    Update an existing item.
    
    - **item_id**: The ID of the item to update
    - **name**: New item name (optional)
    - **description**: New description (optional)
    """
    item = find_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    # Update fields if provided
    if item_update.name is not None:
        if not item_update.name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item name cannot be empty"
            )
        item.name = item_update.name.strip()
    
    if item_update.description is not None:
        item.description = item_update.description
    
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int):
    """
    Delete an item by ID.
    
    - **item_id**: The ID of the item to delete
    """
    global items_db
    item = find_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    items_db = [i for i in items_db if i.id != item_id]
    return None

@app.delete("/items", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_all_items():
    """Delete all items from the database"""
    global items_db
    items_db = []
    return None

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
