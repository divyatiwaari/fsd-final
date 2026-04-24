"""
Validation Test Script
Tests all validation rules implemented in the Flask API
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_test_header(test_name):
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"{'='*70}")

def print_result(response, test_name):
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_valid_student():
    """Test creating a valid student with all correct data"""
    print_test_header("Create Valid Student")
    
    data = {
        "name": "Valid Student",
        "email": f"valid.student.{int(time.time())}@example.com",
        "phone": "9876543210",
        "age": 25,
        "address": "123 Valid Street, Valid City"
    }
    
    response = requests.post(f"{BASE_URL}/api/students", json=data)
    print_result(response, "Valid Student Creation")
    return response.status_code == 201

def test_invalid_email():
    """Test invalid email format"""
    print_test_header("Invalid Email Format")
    
    data = {
        "name": "Test Student",
        "email": "invalid.email",  # Invalid format
        "phone": "9876543210",
        "age": 25,
        "address": "123 Test Street"
    }
    
    response = requests.post(f"{BASE_URL}/api/students", json=data)
    print_result(response, "Invalid Email")
    return response.status_code == 400

def test_invalid_phone():
    """Test invalid phone number"""
    print_test_header("Invalid Phone Number")
    
    data = {
        "name": "Test Student",
        "email": "test@example.com",
        "phone": "123",  # Less than 10 digits
        "age": 25,
        "address": "123 Test Street"
    }
    
    response = requests.post(f"{BASE_URL}/api/students", json=data)
    print_result(response, "Invalid Phone")
    return response.status_code == 400

def test_invalid_age():
    """Test invalid age (outside range)"""
    print_test_header("Invalid Age Range")
    
    data = {
        "name": "Test Student",
        "email": "test@example.com",
        "phone": "9876543210",
        "age": 15,  # Less than 18
        "address": "123 Test Street"
    }
    
    response = requests.post(f"{BASE_URL}/api/students", json=data)
    print_result(response, "Invalid Age")
    return response.status_code == 400

def test_short_name():
    """Test name that's too short"""
    print_test_header("Short Name Validation")
    
    data = {
        "name": "A",  # Only 1 character
        "email": "test@example.com",
        "phone": "9876543210",
        "age": 25,
        "address": "123 Test Street"
    }
    
    response = requests.post(f"{BASE_URL}/api/students", json=data)
    print_result(response, "Short Name")
    return response.status_code == 400

def test_short_address():
    """Test address that's too short"""
    print_test_header("Short Address Validation")
    
    data = {
        "name": "Test Student",
        "email": "test@example.com",
        "phone": "9876543210",
        "age": 25,
        "address": "123"  # Only 3 characters
    }
    
    response = requests.post(f"{BASE_URL}/api/students", json=data)
    print_result(response, "Short Address")
    return response.status_code == 400

def test_missing_fields():
    """Test missing required fields"""
    print_test_header("Missing Required Fields")
    
    data = {
        "name": "Test Student",
        # Missing email, phone, age, address
    }
    
    response = requests.post(f"{BASE_URL}/api/students", json=data)
    print_result(response, "Missing Fields")
    return response.status_code == 400

def test_get_all_students():
    """Test getting all students"""
    print_test_header("Get All Students")
    
    response = requests.get(f"{BASE_URL}/api/students")
    print_result(response, "Get All Students")
    return response.status_code == 200

def test_health_check():
    """Test health check endpoint"""
    print_test_header("Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    print_result(response, "Health Check")
    return response.status_code == 200

def run_all_tests():
    """Run all validation tests"""
    print("\n" + "="*70)
    print("STUDENT CRUD API - VALIDATION TEST SUITE")
    print("="*70)
    
    import time
    
    tests = [
        ("Health Check", test_health_check),
        ("Valid Student", test_valid_student),
        ("Invalid Email", test_invalid_email),
        ("Invalid Phone", test_invalid_phone),
        ("Invalid Age", test_invalid_age),
        ("Short Name", test_short_name),
        ("Short Address", test_short_address),
        ("Missing Fields", test_missing_fields),
        ("Get All Students", test_get_all_students),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASSED" if result else "FAILED"))
        except Exception as e:
            print(f"ERROR: {str(e)}")
            results.append((test_name, "ERROR"))
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"{'Test Name':<30} {'Result':<15}")
    print("-" * 70)
    
    for test_name, result in results:
        status_icon = "✓" if result == "PASSED" else "✗"
        print(f"{test_name:<30} {status_icon} {result:<15}")
    
    passed = sum(1 for _, result in results if result == "PASSED")
    total = len(results)
    print("-" * 70)
    print(f"Total: {passed}/{total} tests passed")
    print("="*70)

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Make sure Flask server is running on http://localhost:5000")
    print("Run the server with: python app.py\n")
    
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Cannot connect to Flask server!")
        print("Please ensure the server is running on http://localhost:5000")
