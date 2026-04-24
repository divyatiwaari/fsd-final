# Unit Testing for Frontend and Backend Modules

A complete full-stack project demonstrating best practices for unit testing both backend and frontend applications. This project is suitable for academic submission and includes a CI/CD pipeline with GitHub Actions.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running Tests](#running-tests)
- [Testing Tools Explanation](#testing-tools-explanation)
- [GitHub Actions CI](#github-actions-ci)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

This project demonstrates a practical implementation of unit testing for a full-stack web application. It includes:

- **Backend**: FastAPI REST API with in-memory data store
- **Frontend**: React application with modern UI
- **Tests**: Comprehensive test suites using pytest and Vitest
- **CI/CD**: GitHub Actions workflow for automated testing

### Problem Statement

Building maintainable software requires robust testing practices. This project shows:
- How to write effective unit tests
- How to test API endpoints
- How to test React components
- How to implement CI/CD pipelines

### Solution

A complete, beginner-friendly implementation of a full-stack application with:
- 25+ backend unit tests (pytest)
- 30+ frontend unit tests (Vitest)
- Automated CI/CD with GitHub Actions
- Clean, well-documented code

---

## ✨ Features

### Backend Features
- ✅ GET /items - Retrieve all items with pagination
- ✅ POST /items - Create new items with validation
- ✅ GET /items/{id} - Retrieve specific item
- ✅ PUT /items/{id} - Update existing items
- ✅ DELETE /items/{id} - Delete specific item
- ✅ DELETE /items - Delete all items
- ✅ CORS support for frontend integration
- ✅ Comprehensive error handling

### Frontend Features
- ✅ Modern React UI with Vite
- ✅ Add items with name and description
- ✅ Display list of items from API
- ✅ Delete items with confirmation
- ✅ Form validation
- ✅ Error and success messages
- ✅ Loading states
- ✅ Responsive design

### Testing Features
- ✅ 25+ backend tests covering all endpoints
- ✅ 30+ frontend component tests
- ✅ Edge case handling tests
- ✅ API integration tests
- ✅ Error handling tests
- ✅ Code coverage reporting

---

## 📁 Project Structure

```
.
├── backend/                          # FastAPI application
│   ├── main.py                      # Main API application with endpoints
│   ├── test_main.py                 # Comprehensive test suite
│   ├── requirements.txt              # Python dependencies
│   └── __pycache__/                 # Python cache (auto-generated)
│
├── frontend/                         # React application
│   ├── src/
│   │   ├── App.jsx                  # Main React component
│   │   ├── App.test.jsx             # Component tests
│   │   ├── main.jsx                 # React entry point
│   │   └── index.css                # Styling
│   ├── index.html                   # HTML entry point
│   ├── package.json                 # Node.js dependencies and scripts
│   ├── vite.config.js               # Vite build configuration
│   ├── vitest.config.js             # Vitest test configuration
│   └── node_modules/                # Dependencies (auto-generated)
│
├── .github/
│   └── workflows/
│       └── test.yml                 # GitHub Actions CI workflow
│
├── README.md                         # This file
└── .gitignore                        # Git ignore file
```

---

## 🚀 Setup Instructions

### Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed
- **Node.js 18+** installed
- **Git** installed
- A **GitHub account** (for CI/CD)

### Step 1: Clone or Download the Project

```bash
# Clone from GitHub (if using Git)
git clone <repository-url>
cd exp\ 16

# Or download and extract the ZIP file
cd exp\ 16
```

### Step 2: Setup Backend

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   pip list
   ```
   You should see: FastAPI, uvicorn, pytest, httpx

### Step 3: Setup Frontend

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Verify installation**
   ```bash
   npm list --depth=0
   ```
   You should see: react, vitest, testing-library packages

---

## 🧪 Running Tests

### Backend Tests

#### Run all backend tests:
```bash
cd backend
pytest test_main.py -v
```

#### Run with coverage report:
```bash
cd backend
pytest test_main.py --cov=. --cov-report=html
```

#### Run specific test class:
```bash
cd backend
pytest test_main.py::TestGETItems -v
```

#### Run with detailed output:
```bash
cd backend
pytest test_main.py -v --tb=long
```

#### Expected Output:
```
test_main.py::test_health_check PASSED
test_main.py::test_get_items_empty PASSED
test_main.py::test_create_item_success PASSED
test_main.py::test_create_item_empty_name PASSED
...
================================ 25 passed in 0.42s ================================
```

### Frontend Tests

#### Run all frontend tests:
```bash
cd frontend
npm test
```

#### Run in watch mode (recommended for development):
```bash
cd frontend
npm test -- --watch
```

#### Run with coverage:
```bash
cd frontend
npm test -- --coverage
```

#### Run specific test file:
```bash
cd frontend
npm test -- App.test.jsx
```

#### Run tests with UI:
```bash
cd frontend
npm run test:ui
```

#### Expected Output:
```
✓ src/App.test.jsx (35)
  ✓ Initial Rendering (4)
    ✓ should render the header with title
    ✓ should render the form section
    ✓ should render the items section
    ✓ should render footer
  ✓ Form Input Behavior (4)
    ✓ should update input value when user types
  ...
  35 passed (1.2s)
```

### Run Both Test Suites

Create a script to run both:

```bash
# Run all tests
cd backend && pytest test_main.py -v && cd ../frontend && npm test
```

---

## 📚 Testing Tools Explanation

### Backend: pytest

**What is pytest?**
- Python testing framework for writing and running unit tests
- Makes it easy to write simple tests with minimal boilerplate
- Provides powerful assertions and fixtures

**Key Features:**
- Simple test discovery (functions starting with `test_`)
- Fixtures for setup/teardown
- Parametrization for testing multiple inputs
- Plugin ecosystem for extensions
- Coverage reporting

**Example Test:**
```python
def test_create_item_success():
    """Test creating a new item successfully"""
    response = client.post("/items", json={"name": "Test Item"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
```

**Why pytest?**
- Pythonic and easy to learn
- Great documentation
- Industry standard for Python testing
- Used in Django, Flask, FastAPI projects

**Test Assertions Used:**
- `assert response.status_code == 201` - Check HTTP status code
- `assert data["name"] == "Test Item"` - Check response data
- `assert item is None` - Check object existence
- `assert "error" in response.json()["detail"]` - Check error messages

### Frontend: Vitest + Testing Library

**What is Vitest?**
- Modern, fast unit test framework for JavaScript/React
- Built on Vite for extremely fast test execution
- Vue/React/Svelte compatible
- Jest-compatible API

**What is Testing Library?**
- Set of utilities for testing React components
- Encourages testing from user's perspective
- Queries elements like real users would (by role, label, text)

**Key Features:**
- Extremely fast test execution (Vite-based)
- React Testing Library best practices
- User-centric testing approach
- Mock/spy functionality
- Code coverage reporting

**Example Test:**
```javascript
it('should update input value when user types', async () => {
  const user = userEvent.setup()
  render(<App />)
  
  const nameInput = screen.getByTestId('item-name-input')
  await user.type(nameInput, 'Test Item')
  
  expect(nameInput.value).toBe('Test Item')
})
```

**Why Vitest + Testing Library?**
- Testing Library follows best practices (test behavior, not implementation)
- Vitest is much faster than Jest
- Modern JavaScript support
- Great for React component testing

**Testing Approach:**
- `render()` - Render component in a virtual DOM
- `screen.getByTestId()` - Query elements
- `userEvent.setup()` - Simulate user interactions
- `waitFor()` - Wait for async operations
- `expect()` - Assert expected behavior

### Comparison: Testing Tools

| Aspect | pytest | Vitest |
|--------|--------|--------|
| Language | Python | JavaScript |
| Target | Backend/APIs | Frontend/React |
| Speed | Fast | Very Fast |
| Learning Curve | Gentle | Gentle |
| Ecosystem | Large | Growing |
| Mocking | Built-in | Built-in |
| Coverage | pytest-cov | @vitest/coverage-v8 |

---

## 🔄 GitHub Actions CI

### What is GitHub Actions?

GitHub Actions is a continuous integration/continuous deployment (CI/CD) platform that:
- Automatically runs tests on every push and pull request
- Ensures code quality before merging
- Runs on multiple Python and Node.js versions
- Provides badges showing test status

### Workflow Overview

The `.github/workflows/test.yml` file defines:

1. **Trigger Events**
   - Runs on `push` to `main` and `develop` branches
   - Runs on `pull_request` to `main` and `develop` branches

2. **Jobs**
   - `backend-tests`: Runs pytest on Python 3.9 and 3.11
   - `frontend-tests`: Runs vitest on Node.js 18.x and 20.x
   - `code-quality`: Lints both codebases
   - `test-summary`: Reports overall status

3. **Steps in Each Job**
   - Checkout code
   - Setup environment (Python/Node.js)
   - Install dependencies
   - Run tests
   - Generate coverage reports
   - Upload results

### How to Set Up GitHub Actions

#### Step 1: Push Code to GitHub

```bash
# Initialize git repo (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Add unit testing project"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Step 2: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click "Actions" tab
3. GitHub should auto-detect `.github/workflows/test.yml`
4. Workflow will run automatically on next push

#### Step 3: View Results

1. Click "Actions" tab
2. Select the workflow run
3. View logs for each job
4. Check for ✅ or ❌ status

### Workflow Badges

Add this to your README to show test status:

```markdown
[![Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/test.yml)
```

### Example Workflow Execution

```
✅ backend-tests (Python 3.9)
  ✓ Install dependencies
  ✓ Run backend tests
  ✓ pytest test_main.py -v (25 passed)

✅ backend-tests (Python 3.11)
  ✓ Install dependencies
  ✓ Run backend tests
  ✓ pytest test_main.py -v (25 passed)

✅ frontend-tests (Node 18.x)
  ✓ Install dependencies
  ✓ Run frontend tests
  ✓ npm test (35 passed)

✅ frontend-tests (Node 20.x)
  ✓ Install dependencies
  ✓ Run frontend tests
  ✓ npm test (35 passed)

✅ test-summary
  All tests passed!
```

---

## 📖 API Documentation

### Base URL
- Local: `http://localhost:8000`
- Production: `https://api.example.com`

### Endpoints Overview

#### 1. GET /items
Retrieve all items with optional pagination.

**Request:**
```bash
GET /items?skip=0&limit=10
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Item 1",
    "description": "Description of item 1"
  },
  {
    "id": 2,
    "name": "Item 2",
    "description": null
  }
]
```

**Query Parameters:**
- `skip` (int, default: 0) - Number of items to skip
- `limit` (int, default: 10) - Maximum items to return

#### 2. POST /items
Create a new item.

**Request:**
```bash
POST /items
Content-Type: application/json

{
  "name": "New Item",
  "description": "Item description"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "New Item",
  "description": "Item description"
}
```

**Validation:**
- `name` is required and cannot be empty
- `description` is optional

**Error (400 Bad Request):**
```json
{
  "detail": "Item name cannot be empty"
}
```

#### 3. GET /items/{id}
Retrieve a specific item by ID.

**Request:**
```bash
GET /items/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Item 1",
  "description": "Description"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Item with id 1 not found"
}
```

#### 4. PUT /items/{id}
Update an existing item.

**Request:**
```bash
PUT /items/1
Content-Type: application/json

{
  "name": "Updated Item",
  "description": "Updated description"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Item",
  "description": "Updated description"
}
```

**Note:** Both `name` and `description` are optional. Only provided fields will be updated.

#### 5. DELETE /items/{id}
Delete a specific item.

**Request:**
```bash
DELETE /items/1
```

**Response (204 No Content)**

**Error (404 Not Found):**
```json
{
  "detail": "Item with id 1 not found"
}
```

#### 6. DELETE /items
Delete all items.

**Request:**
```bash
DELETE /items
```

**Response (204 No Content)**

#### 7. GET /health
Health check endpoint.

**Request:**
```bash
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## 🧬 Test Coverage

### Backend Test Coverage

**Total Tests:** 25+

**Categories:**
1. **Health Check (1 test)**
   - Health endpoint verification

2. **GET /items (4 tests)**
   - Empty list handling
   - Pagination functionality
   - Multiple items retrieval

3. **POST /items (6 tests)**
   - Successful creation
   - Name validation
   - Whitespace trimming
   - Unique ID generation

4. **GET /items/{id} (3 tests)**
   - Successful retrieval
   - Not found error handling

5. **PUT /items/{id} (5 tests)**
   - Name and description updates
   - Partial updates
   - Error handling

6. **DELETE /items/{id} (3 tests)**
   - Successful deletion
   - Not found error handling

7. **DELETE /items (2 tests)**
   - Delete all items

8. **Integration Tests (2+ tests)**
   - Full CRUD workflow

### Frontend Test Coverage

**Total Tests:** 35+

**Categories:**
1. **Rendering (4 tests)**
   - Header rendering
   - Form rendering
   - Items list rendering
   - Footer rendering

2. **Form Input (4 tests)**
   - Text input handling
   - Textarea handling
   - Input clearing

3. **Form Submission (5 tests)**
   - Valid submission
   - Empty name validation
   - Success messages
   - Error handling

4. **Items List (6 tests)**
   - Empty state display
   - Item rendering
   - Item details display
   - Loading states

5. **Delete Functionality (5 tests)**
   - Successful deletion
   - API integration
   - List update after deletion

6. **API Error Handling (3 tests)**
   - Network errors
   - API errors
   - Error messages

7. **Integration Tests (3+ tests)**
   - Full CRUD workflow
   - Multiple items handling

---

## 🔧 Development

### Running the Application Locally

#### Start Backend
```bash
cd backend
python -m uvicorn main:app --reload
```

Visit: `http://localhost:8000/docs` (Swagger UI)

#### Start Frontend (in another terminal)
```bash
cd frontend
npm run dev
```

Visit: `http://localhost:3000`

### Making Changes

1. **Backend Changes**
   - Edit `backend/main.py`
   - Server auto-reloads with `--reload` flag
   - Run tests: `cd backend && pytest test_main.py -v`

2. **Frontend Changes**
   - Edit `frontend/src/App.jsx`
   - Browser auto-refreshes with Vite dev server
   - Run tests: `cd frontend && npm test`

### Adding New Tests

**For Backend (pytest):**
```python
def test_new_feature():
    """Test description"""
    response = client.get("/endpoint")
    assert response.status_code == 200
```

**For Frontend (Vitest):**
```javascript
it('should test new feature', async () => {
  const user = userEvent.setup()
  render(<App />)
  
  const element = screen.getByRole('button', { name: /test/i })
  await user.click(element)
  
  expect(element).toHaveTextContent('updated')
})
```

---

## 📊 Code Quality

### Backend Code Quality
- PEP 8 compliant (Python style guide)
- Comprehensive docstrings
- Type hints where applicable
- Error handling with proper status codes

### Frontend Code Quality
- ESLint compatible JavaScript
- Descriptive component names
- Accessibility attributes (aria-labels, roles)
- Clean, commented code

---

## 🎓 Learning Resources

### Backend Testing (pytest)
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes)

### Frontend Testing (Vitest)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library Docs](https://testing-library.com/docs/react-testing-library/intro/)
- [React Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new functionality
4. Run all tests and ensure they pass
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**Before submitting PR:**
- All tests must pass
- New features must have tests
- Code must follow style guidelines
- Update README if needed

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Troubleshooting

### Backend Issues

**Issue: pytest not found**
```bash
# Solution: Install pytest
pip install pytest pytest-cov httpx
```

**Issue: Port 8000 already in use**
```bash
# Use different port
python -m uvicorn main:app --port 8001
```

**Issue: Module 'main' not found**
```bash
# Ensure you're in backend directory
cd backend
pytest test_main.py -v
```

### Frontend Issues

**Issue: npm packages not installing**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue: Vitest not running**
```bash
# Install dev dependencies
npm install --save-dev vitest @testing-library/react jsdom
```

**Issue: Port 3000 already in use**
```bash
# Vite will automatically use next available port
npm run dev
```

### GitHub Actions Issues

**Issue: Workflow not running**
- Check workflow file syntax (YAML format)
- Ensure file is at `.github/workflows/test.yml`
- Push code to trigger workflow

**Issue: Tests fail in CI but pass locally**
- Check Python/Node.js version differences
- Verify all dependencies in requirements.txt/package.json
- Check for hardcoded paths or environment variables

---

## 📞 Contact & Support

For questions or issues:
1. Check this README
2. Review test files for examples
3. Check GitHub Issues
4. Create a new issue with details

---

**Happy Testing! 🎉**

---

*Last Updated: April 2026*
