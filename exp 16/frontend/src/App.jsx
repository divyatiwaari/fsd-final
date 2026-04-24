import React, { useState, useEffect } from 'react'
import './App.css'

/**
 * Main App component that manages items
 * Features:
 * - Display list of items fetched from backend
 * - Add new items via form
 * - Delete items
 */
function App() {
  const [items, setItems] = useState([])
  const [itemName, setItemName] = useState('')
  const [itemDescription, setItemDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // API base URL
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  // Fetch items from backend on component mount
  useEffect(() => {
    fetchItems()
  }, [])

  /**
   * Fetch all items from the backend API
   */
  const fetchItems = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await fetch(`${API_URL}/items`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch items')
      }
      
      const data = await response.json()
      setItems(data)
    } catch (err) {
      setError(err.message || 'Failed to fetch items')
      console.error('Fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  /**
   * Handle form submission to add a new item
   */
  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validation
    if (!itemName.trim()) {
      setError('Item name cannot be empty')
      return
    }

    try {
      setLoading(true)
      setError('')
      setSuccess('')

      const response = await fetch(`${API_URL}/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: itemName,
          description: itemDescription || null
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to create item')
      }

      const newItem = await response.json()
      
      // Add item to list and reset form
      setItems([...items, newItem])
      setItemName('')
      setItemDescription('')
      setSuccess('Item added successfully!')
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.message || 'Failed to create item')
      console.error('Submit error:', err)
    } finally {
      setLoading(false)
    }
  }

  /**
   * Handle deleting an item
   */
  const handleDelete = async (itemId) => {
    try {
      setError('')
      const response = await fetch(`${API_URL}/items/${itemId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error('Failed to delete item')
      }

      // Remove item from list
      setItems(items.filter(item => item.id !== itemId))
      setSuccess('Item deleted successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.message || 'Failed to delete item')
      console.error('Delete error:', err)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Items Manager</h1>
        <p>A simple application to manage your items</p>
      </header>

      <main className="main-content">
        {/* Alert Messages */}
        {error && <div className="alert alert-error" role="alert">{error}</div>}
        {success && <div className="alert alert-success" role="alert">{success}</div>}

        {/* Form Section */}
        <section className="form-section">
          <h2>Add New Item</h2>
          <form onSubmit={handleSubmit} className="item-form">
            <div className="form-group">
              <label htmlFor="item-name">Item Name *</label>
              <input
                id="item-name"
                data-testid="item-name-input"
                type="text"
                value={itemName}
                onChange={(e) => setItemName(e.target.value)}
                placeholder="Enter item name"
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="item-description">Description</label>
              <textarea
                id="item-description"
                data-testid="item-description-input"
                value={itemDescription}
                onChange={(e) => setItemDescription(e.target.value)}
                placeholder="Enter item description (optional)"
                disabled={loading}
                rows="3"
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              data-testid="submit-button"
            >
              {loading ? 'Adding...' : 'Add Item'}
            </button>
          </form>
        </section>

        {/* Items List Section */}
        <section className="items-section">
          <h2>Items List</h2>
          {loading && items.length === 0 ? (
            <p className="loading-text">Loading items...</p>
          ) : items.length === 0 ? (
            <p className="empty-text">No items yet. Add one to get started!</p>
          ) : (
            <div className="items-grid" data-testid="items-list">
              {items.map((item) => (
                <div key={item.id} className="item-card" data-testid={`item-${item.id}`}>
                  <div className="item-content">
                    <h3 className="item-name" data-testid={`item-name-${item.id}`}>
                      {item.name}
                    </h3>
                    {item.description && (
                      <p className="item-description" data-testid={`item-description-${item.id}`}>
                        {item.description}
                      </p>
                    )}
                    <p className="item-id">ID: {item.id}</p>
                  </div>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(item.id)}
                    disabled={loading}
                    data-testid={`delete-button-${item.id}`}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>Items Manager v1.0.0 | Built with React + Vite</p>
      </footer>
    </div>
  )
}

export default App
