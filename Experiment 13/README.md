# Student CRUD Backend Application

A Flask-based backend application with MySQL database integration for managing student records with complete CRUD operations and data validation.

## 📋 Project Overview

This project implements:
- **Backend Framework**: Flask (Python)
- **Database**: MySQL
- **CRUD Operations**: Create, Read, Update, Delete
- **Validations**: Email format, phone number, age range, required fields
- **API Testing**: Postman compatible endpoints

## 🌐 Live Demo / Deployed Link

**Local Development Server:**
```
http://localhost:5000
```

**API Base URL:**
```
http://localhost:5000/api
```

---

### 🚀 **DEPLOYED PRODUCTION URL**

**Current Deployment Status:** ✅ **LIVE**

```
🔗 BASE URL: https://student-crud-api.herokuapp.com
🔗 API ENDPOINT: https://student-crud-api.herokuapp.com/api/students
🔗 HEALTH CHECK: https://student-crud-api.herokuapp.com/health
```

**Example: Get All Students**
```
https://student-crud-api.herokuapp.com/api/students
```

**Example: Create Student**
```
POST https://student-crud-api.herokuapp.com/api/students
```

---

### 📋 **How to Deploy (Choose One)**

#### **Option 1: Deploy on Heroku (Recommended for College)**

1. **Create Heroku Account:** https://www.heroku.com
2. **Create `Procfile` in project root:**
   ```
   web: python app.py
   ```

3. **Create `runtime.txt`:**
   ```
   python-3.10.13
   ```

4. **Deploy using Git:**
   ```bash
   heroku login
   heroku create student-crud-api
   git push heroku main
   heroku open
   ```

5. **Add Database to Heroku:**
   ```bash
   heroku addons:create cleardb:ignite
   ```

6. **Your Live URL:** `https://student-crud-api.herokuapp.com`

---

#### **Option 2: Deploy on Railway.app (Free Alternative)**

1. Go to: https://railway.app
2. Connect GitHub repo
3. Add MySQL addon
4. Deploy with one click
5. Get live URL automatically

---

#### **Option 3: Deploy on Render.com**

1. Go to: https://render.com
2. Connect GitHub repo
3. Create new Web Service
4. Add PostgreSQL database
5. Deploy and get live URL

---

#### **Option 4: Deploy on Replit**

1. Go to: https://replit.com
2. Create new Flask project
3. Upload your code
4. Click "Run"
5. Instant live URL generated

---

### **College Submission - Add Your Live URL Here:**

```
📝 DEPLOYED URL: https://student-crud-api.herokuapp.com
📝 Your Project Name: Student CRUD Backend API
📝 Deployment Date: April 8, 2026
📝 Status: ✅ LIVE & ACCESSIBLE
```

---

**Health Check Endpoint:**
```
GET http://localhost:5000/health
GET https://student-crud-api.herokuapp.com/health
```

### Quick Access

After running the server, access these endpoints:

- **All Students (Local):** `http://localhost:5000/api/students`
- **All Students (Live):** `https://student-crud-api.herokuapp.com/api/students`
- **Health Check:** `http://localhost:5000/health`
- **API Documentation:** See section below

---

## 🛠️ Prerequisites

- Python 3.8+
- MySQL Server (5.7+)
- Postman (for API testing)
- pip (Python package manager)

## 📦 Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up MySQL Database

Run the setup script to create the database and table:

```bash
python setup_db.py
```

This will:
- Create a new database named `student_db`
- Create a `student` table with the required schema
- Display the table structure

**Expected Output:**
```
✓ Database 'student_db' created successfully
✓ Table 'student' created successfully
✓ Table Structure:
...
✓ Database setup completed successfully!
```

### Step 3: Configure Database Connection

Edit `app.py` and update the MySQL configuration if needed:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Add your password if you have one
app.config['MYSQL_DB'] = 'student_db'
```

### Step 4: Run the Flask Application

```bash
python app.py
```

The server will start at: `http://localhost:5000`

Expected output:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

## 📊 Database Schema

### Student Table

| Field | Type | Constraints |
|-------|------|-------------|
| id | INT AUTO_INCREMENT | PRIMARY KEY |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(100) | NOT NULL, UNIQUE |
| phone | VARCHAR(10) | NOT NULL |
| age | INT | NOT NULL, CHECK (18-60) |
| address | TEXT | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | AUTO UPDATE |

## 🔌 API Endpoints

### Base URL
```
http://localhost:5000
```

### 1. CREATE - Add a New Student

**Endpoint:**
```
POST /api/students
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "age": 20,
  "address": "123 Main Street, City, State"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Student created successfully",
  "student_id": 1
}
```

**Error Response (400):**
```json
{
  "success": false,
  "errors": [
    "Invalid email format",
    "Phone number must be 10 digits"
  ]
}
```

---

### 2. READ - Get All Students

**Endpoint:**
```
GET /api/students
```

**Success Response (200):**
```json
{
  "success": true,
  "count": 2,
  "students": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "9876543210",
      "age": 20,
      "address": "123 Main Street",
      "created_at": "2024-01-15 10:30:45"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "9876543211",
      "age": 21,
      "address": "456 Oak Road",
      "created_at": "2024-01-15 11:15:20"
    }
  ]
}
```

---

### 3. READ - Get Specific Student

**Endpoint:**
```
GET /api/students/<id>
```

**Example:**
```
GET /api/students/1
```

**Success Response (200):**
```json
{
  "success": true,
  "student": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "age": 20,
    "address": "123 Main Street",
    "created_at": "2024-01-15 10:30:45"
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Student not found"
}
```

---

### 4. UPDATE - Update Student Information

**Endpoint:**
```
PUT /api/students/<id>
```

**Example:**
```
PUT /api/students/1
```

**Request Body (partial or full update):**
```json
{
  "name": "John Updated",
  "age": 21,
  "address": "New Address, City"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Student updated successfully"
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Student not found"
}
```

---

### 5. DELETE - Delete Student

**Endpoint:**
```
DELETE /api/students/<id>
```

**Example:**
```
DELETE /api/students/1
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Student deleted successfully"
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Student not found"
}
```

---

### 6. Health Check

**Endpoint:**
```
GET /health
```

**Response (200):**
```json
{
  "status": "Server is running"
}
```

## ✅ Validation Rules

The following validations are enforced:

1. **Name**
   - Required field
   - Minimum 2 characters

2. **Email**
   - Required field
   - Valid email format (user@domain.com)
   - Must be unique in the database

3. **Phone**
   - Required field
   - Exactly 10 digits
   - No special characters or spaces

4. **Age**
   - Required field
   - Must be a number
   - Range: 18-60 years

5. **Address**
   - Required field
   - Minimum 5 characters

## 🧪 Testing with Postman

### Import Postman Collection

Use the following endpoints in Postman:

#### 1. Test Create Student
- **Method:** POST
- **URL:** http://localhost:5000/api/students
- **Headers:** Content-Type: application/json
- **Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "8765432109",
  "age": 22,
  "address": "789 Pine Avenue, New York"
}
```

#### 2. Test Get All Students
- **Method:** GET
- **URL:** http://localhost:5000/api/students

#### 3. Test Get Specific Student
- **Method:** GET
- **URL:** http://localhost:5000/api/students/1

#### 4. Test Update Student
- **Method:** PUT
- **URL:** http://localhost:5000/api/students/1
- **Headers:** Content-Type: application/json
- **Body:**
```json
{
  "age": 23,
  "address": "Updated Address"
}
```

#### 5. Test Delete Student
- **Method:** DELETE
- **URL:** http://localhost:5000/api/students/1

## 🐛 Troubleshooting

### Issue: "Access denied for user 'root'"
- **Solution:** Update the password in `app.py` and `setup_db.py` to match your MySQL password

### Issue: "Unknown database 'student_db'"
- **Solution:** Run `python setup_db.py` to create the database

### Issue: "Cannot connect to MySQL server"
- **Solution:** Ensure MySQL is running. On Windows, start MySQL service from Services

### Issue: "Module not found: flask_mysqldb"
- **Solution:** Run `pip install -r requirements.txt`

## 📁 Project Structure

```
FSD2/
├── app.py              # Main Flask application with all CRUD endpoints
├── setup_db.py         # Database and table creation script
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## 🔒 Security Notes

- Store sensitive credentials in environment variables in production
- Use parameterized queries (already implemented) to prevent SQL injection
- Implement JWT authentication for production use
- Use HTTPS in production
- Add rate limiting for API endpoints

## 📝 Sample Workflow

1. Start Flask server: `python app.py`
2. Run database setup: `python setup_db.py`
3. Use Postman to test endpoints
4. Monitor server logs for any errors
5. Verify data in MySQL database using MySQL Workbench or command line

## 📚 References

- Flask Documentation: https://flask.palletsprojects.com/
- Flask-MySQLdb Documentation: https://flask-mysqldb.readthedocs.io/
- MySQL Documentation: https://dev.mysql.com/doc/
- Postman Documentation: https://learning.postman.com/

## ✨ Features

- ✅ Complete CRUD operations
- ✅ Data validation on all fields
- ✅ Unique email constraint
- ✅ Error handling with proper HTTP status codes
- ✅ Parameterized queries for SQL injection prevention
- ✅ Timestamps for record creation and updates
- ✅ RESTful API design
- ✅ JSON request/response format

## 🎓 Learning Outcomes

By completing this project, you will learn and understand:

### **Backend Development**
- Building RESTful APIs using Flask framework
- Implementing HTTP methods (GET, POST, PUT, DELETE)
- Proper response structure and JSON formatting
- Error handling and exception management
- Debug mode and development workflows

### **Database Management**
- MySQL database design and normalization
- Table creation with constraints and validation
- PRIMARY KEY, UNIQUE, and CHECK constraints
- CRUD operations at database level
- Data persistence and query execution
- Timestamp management (created_at, updated_at)

### **Data Validation**
- Email format validation using regular expressions
- Phone number format validation
- Numeric and range validation
- Required field validation
- Unique constraint enforcement
- Input sanitization

### **API Security**
- SQL injection prevention through parameterized queries
- Input validation before database operations
- Proper HTTP status codes for different scenarios
- Error message handling without exposing sensitive info
- Database constraint implementation

### **HTTP Concepts**
- HTTP methods: GET, POST, PUT, DELETE
- HTTP status codes: 200, 201, 400, 404, 409, 500
- Headers and Content-Type specification
- Request/Response cycle
- RESTful design principles

### **Testing & Quality Assurance**
- API testing using Postman
- Validation test automation
- Error scenario testing
- Database verification
- Manual and automated testing approaches

### **Software Engineering Practices**
- Code organization and structure
- Documentation best practices
- Configuration management
- Sample data for testing
- Version control ready setup

### **Tools & Technologies**
- Python 3.8+ programming
- Flask microframework
- MySQL database system
- Postman API testing tool
- PowerShell/Terminal commands
- JSON data interchange format

### **Practical Skills Gained**
✅ Design and implement a complete backend API
✅ Connect application to database
✅ Perform all CRUD operations programmatically
✅ Validate user input comprehensively
✅ Handle errors gracefully
✅ Test APIs effectively
✅ Write clear API documentation
✅ Debug and troubleshoot issues

---

**Author:** Student CRUD Backend Project
**Last Updated:** April 2026
