/**
 * Unit tests for the React frontend application using Vitest + Testing Library
 *
 * This test suite covers:
 * - Form input behavior
 * - Form submission
 * - Item list rendering
 * - Error handling
 * - API integration (mocked)
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

/**
 * Mock fetch API
 */
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()
    fetch.mockClear()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  // ============= Rendering Tests =============

  describe('Initial Rendering', () => {
    it('should render the header with title', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      expect(screen.getByText('Items Manager')).toBeInTheDocument()
      expect(screen.getByText('A simple application to manage your items')).toBeInTheDocument()
    })

    it('should render the form section', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      expect(screen.getByText('Add New Item')).toBeInTheDocument()
      expect(screen.getByLabelText('Item Name *')).toBeInTheDocument()
      expect(screen.getByLabelText('Description')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /Add Item/i })).toBeInTheDocument()
    })

    it('should render the items section', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      expect(screen.getByText('Items List')).toBeInTheDocument()
    })

    it('should render footer', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      expect(screen.getByText(/Items Manager v1.0.0/)).toBeInTheDocument()
    })
  })

  // ============= Form Input Tests =============

  describe('Form Input Behavior', () => {
    beforeEach(() => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
    })

    it('should update input value when user types', async () => {
      const user = userEvent.setup()
      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      await user.type(nameInput, 'Test Item')

      expect(nameInput.value).toBe('Test Item')
    })

    it('should update description when user types', async () => {
      const user = userEvent.setup()
      render(<App />)

      const descInput = screen.getByTestId('item-description-input')
      await user.type(descInput, 'Test Description')

      expect(descInput.value).toBe('Test Description')
    })

    it('should accept multiple lines in description', async () => {
      const user = userEvent.setup()
      render(<App />)

      const descInput = screen.getByTestId('item-description-input')
      await user.type(descInput, 'Line 1{Enter}Line 2')

      expect(descInput.value).toContain('Line 1')
      expect(descInput.value).toContain('Line 2')
    })

    it('should clear input fields after successful submission', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'Test Item', description: 'Test' })
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const descInput = screen.getByTestId('item-description-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Test Item')
      await user.type(descInput, 'Test Description')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(nameInput.value).toBe('')
        expect(descInput.value).toBe('')
      })
    })
  })

  // ============= Form Submission Tests =============

  describe('Form Submission', () => {
    it('should not submit when name is empty', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      const submitBtn = screen.getByTestId('submit-button')
      await user.click(submitBtn)

      expect(screen.getByText('Item name cannot be empty')).toBeInTheDocument()
      expect(fetch).toHaveBeenCalledTimes(1) // Only initial fetch
    })

    it('should not submit when name is only whitespace', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, '   ')
      await user.click(submitBtn)

      expect(screen.getByText('Item name cannot be empty')).toBeInTheDocument()
    })

    it('should submit form with name and description', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'Item 1', description: 'Desc' })
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const descInput = screen.getByTestId('item-description-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Item 1')
      await user.type(descInput, 'Desc')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          expect.stringContaining('/items'),
          expect.objectContaining({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: expect.stringContaining('Item 1')
          })
        )
      })
    })

    it('should submit form with only name (no description)', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'Item 1', description: null })
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Item 1')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          expect.stringContaining('/items'),
          expect.objectContaining({ method: 'POST' })
        )
      })
    })

    it('should show success message after submission', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'Test Item', description: null })
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Test Item')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(screen.getByText('Item added successfully!')).toBeInTheDocument()
      })
    })

    it('should show error message on submission failure', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Server error' })
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Test Item')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(screen.getByText('Server error')).toBeInTheDocument()
      })
    })

    it('should disable form during submission', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ id: 1, name: 'Item', description: null })
        }), 100))
      )

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Test Item')
      await user.click(submitBtn)

      expect(nameInput).toBeDisabled()
      expect(submitBtn).toBeDisabled()
    })
  })

  // ============= Items List Rendering Tests =============

  describe('Items List Rendering', () => {
    it('should display empty state message when no items', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('No items yet. Add one to get started!')).toBeInTheDocument()
      })
    })

    it('should display items fetched from API', async () => {
      const items = [
        { id: 1, name: 'Item 1', description: 'Desc 1' },
        { id: 2, name: 'Item 2', description: 'Desc 2' }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Item 1')).toBeInTheDocument()
        expect(screen.getByText('Item 2')).toBeInTheDocument()
        expect(screen.getByText('Desc 1')).toBeInTheDocument()
        expect(screen.getByText('Desc 2')).toBeInTheDocument()
      })
    })

    it('should display items without descriptions', async () => {
      const items = [
        { id: 1, name: 'Item 1', description: null }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Item 1')).toBeInTheDocument()
        expect(screen.queryByTestId('item-description-1')).not.toBeInTheDocument()
      })
    })

    it('should display item IDs', async () => {
      const items = [
        { id: 42, name: 'Item 1', description: null }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('ID: 42')).toBeInTheDocument()
      })
    })

    it('should display loading state during fetch', async () => {
      fetch.mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => []
        }), 100))
      )

      render(<App />)

      expect(screen.getByText('Loading items...')).toBeInTheDocument()

      await waitFor(() => {
        expect(screen.queryByText('Loading items...')).not.toBeInTheDocument()
      })
    })

    it('should add newly created item to list', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'New Item', description: null })
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'New Item')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(screen.getByText('New Item')).toBeInTheDocument()
      })
    })
  })

  // ============= Delete Item Tests =============

  describe('Delete Item Functionality', () => {
    it('should delete item when delete button is clicked', async () => {
      const user = userEvent.setup()
      const items = [
        { id: 1, name: 'Item 1', description: null }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })
      fetch.mockResolvedValueOnce({
        ok: true
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Item 1')).toBeInTheDocument()
      })

      const deleteBtn = screen.getByTestId('delete-button-1')
      await user.click(deleteBtn)

      await waitFor(() => {
        expect(screen.queryByText('Item 1')).not.toBeInTheDocument()
      })
    })

    it('should call delete API with correct item ID', async () => {
      const user = userEvent.setup()
      const items = [
        { id: 123, name: 'Item', description: null }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })
      fetch.mockResolvedValueOnce({
        ok: true
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Item')).toBeInTheDocument()
      })

      const deleteBtn = screen.getByTestId('delete-button-123')
      await user.click(deleteBtn)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          expect.stringContaining('/items/123'),
          expect.objectContaining({ method: 'DELETE' })
        )
      })
    })

    it('should show success message on delete', async () => {
      const user = userEvent.setup()
      const items = [
        { id: 1, name: 'Item', description: null }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })
      fetch.mockResolvedValueOnce({
        ok: true
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Item')).toBeInTheDocument()
      })

      const deleteBtn = screen.getByTestId('delete-button-1')
      await user.click(deleteBtn)

      await waitFor(() => {
        expect(screen.getByText('Item deleted successfully!')).toBeInTheDocument()
      })
    })

    it('should show error message on delete failure', async () => {
      const user = userEvent.setup()
      const items = [
        { id: 1, name: 'Item', description: null }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })
      fetch.mockResolvedValueOnce({
        ok: false
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Item')).toBeInTheDocument()
      })

      const deleteBtn = screen.getByTestId('delete-button-1')
      await user.click(deleteBtn)

      await waitFor(() => {
        expect(screen.getByText('Failed to delete item')).toBeInTheDocument()
      })
    })

    it('should remove only the deleted item from list', async () => {
      const user = userEvent.setup()
      const items = [
        { id: 1, name: 'Item 1', description: null },
        { id: 2, name: 'Item 2', description: null }
      ]
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => items
      })
      fetch.mockResolvedValueOnce({
        ok: true
      })

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Item 1')).toBeInTheDocument()
        expect(screen.getByText('Item 2')).toBeInTheDocument()
      })

      const deleteBtn = screen.getByTestId('delete-button-1')
      await user.click(deleteBtn)

      await waitFor(() => {
        expect(screen.queryByText('Item 1')).not.toBeInTheDocument()
        expect(screen.getByText('Item 2')).toBeInTheDocument()
      })
    })
  })

  // ============= API Error Handling Tests =============

  describe('API Error Handling', () => {
    it('should handle fetch error on initial load', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)

      await waitFor(() => {
        expect(screen.getByText('Failed to fetch items')).toBeInTheDocument()
      })
    })

    it('should handle fetch error on submit', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Item')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(screen.getByText('Failed to create item')).toBeInTheDocument()
      })
    })

    it('should handle API error response on submit', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Item already exists' })
      })

      render(<App />)

      const nameInput = screen.getByTestId('item-name-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Item')
      await user.click(submitBtn)

      await waitFor(() => {
        expect(screen.getByText('Item already exists')).toBeInTheDocument()
      })
    })
  })

  // ============= Integration Tests =============

  describe('Integration Tests', () => {
    it('should complete full workflow: create, display, delete', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'Test Item', description: 'Test' })
      })
      fetch.mockResolvedValueOnce({
        ok: true
      })

      render(<App />)

      // Step 1: Fill form
      const nameInput = screen.getByTestId('item-name-input')
      const descInput = screen.getByTestId('item-description-input')
      const submitBtn = screen.getByTestId('submit-button')

      await user.type(nameInput, 'Test Item')
      await user.type(descInput, 'Test')

      // Step 2: Submit form
      await user.click(submitBtn)

      // Step 3: Verify item appears in list
      await waitFor(() => {
        expect(screen.getByText('Test Item')).toBeInTheDocument()
        expect(screen.getByText('Test')).toBeInTheDocument()
      })

      // Step 4: Delete item
      const deleteBtn = screen.getByTestId('delete-button-1')
      await user.click(deleteBtn)

      // Step 5: Verify item is removed
      await waitFor(() => {
        expect(screen.queryByText('Test Item')).not.toBeInTheDocument()
      })
    })

    it('should handle multiple items', async () => {
      const user = userEvent.setup()
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })

      render(<App />)

      // Create first item
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'Item 1', description: null })
      })

      const nameInput = screen.getByTestId('item-name-input')
      await user.type(nameInput, 'Item 1')
      await user.click(screen.getByTestId('submit-button'))

      await waitFor(() => {
        expect(screen.getByText('Item 1')).toBeInTheDocument()
      })

      // Create second item
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 2, name: 'Item 2', description: null })
      })

      const newInput = screen.getByTestId('item-name-input')
      await user.type(newInput, 'Item 2')
      await user.click(screen.getByTestId('submit-button'))

      await waitFor(() => {
        expect(screen.getByText('Item 1')).toBeInTheDocument()
        expect(screen.getByText('Item 2')).toBeInTheDocument()
      })
    })
  })
})
