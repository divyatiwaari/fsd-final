from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import re
import os

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Change if you have a password
app.config['MYSQL_DB'] = 'student_db'

mysql = MySQL(app)

# ======================== VALIDATION FUNCTIONS ========================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (10 digits)"""
    return phone.isdigit() and len(phone) == 10

def validate_student_data(data, is_update=False):
    """Validate student data"""
    errors = []
    
    if not is_update or 'name' in data:
        if 'name' not in data or not data['name']:
            errors.append('Name is required')
        elif len(data['name']) < 2:
            errors.append('Name must be at least 2 characters long')
    
    if not is_update or 'email' in data:
        if 'email' not in data or not data['email']:
            errors.append('Email is required')
        elif not validate_email(data['email']):
            errors.append('Invalid email format')
    
    if not is_update or 'phone' in data:
        if 'phone' not in data or not data['phone']:
            errors.append('Phone number is required')
        elif not validate_phone(data['phone']):
            errors.append('Phone number must be 10 digits')
    
    if not is_update or 'age' in data:
        if 'age' not in data:
            errors.append('Age is required')
        else:
            try:
                age = int(data['age'])
                if age < 18 or age > 60:
                    errors.append('Age must be between 18 and 60')
            except ValueError:
                errors.append('Age must be a number')
    
    if not is_update or 'address' in data:
        if 'address' not in data or not data['address']:
            errors.append('Address is required')
        elif len(data['address']) < 5:
            errors.append('Address must be at least 5 characters long')
    
    return errors

# ======================== CREATE ENDPOINTS ========================

@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        # Validate data
        errors = validate_student_data(data)
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Check if email already exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Email already exists'}), 409
        
        # Insert student
        cursor.execute("""
            INSERT INTO student (name, email, phone, age, address, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (data['name'], data['email'], data['phone'], data['age'], data['address']))
        
        mysql.connection.commit()
        student_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({
            'success': True,
            'message': 'Student created successfully',
            'student_id': student_id
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================== READ ENDPOINTS ========================

@app.route('/api/students', methods=['GET'])
def get_all_students():
    """Get all students"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, phone, age, address, created_at FROM student ORDER BY id DESC")
        students = cursor.fetchall()
        cursor.close()
        
        student_list = []
        for student in students:
            student_list.append({
                'id': student[0],
                'name': student[1],
                'email': student[2],
                'phone': student[3],
                'age': student[4],
                'address': student[5],
                'created_at': str(student[6])
            })
        
        return jsonify({'success': True, 'count': len(student_list), 'students': student_list}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student by ID"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, phone, age, address, created_at FROM student WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        cursor.close()
        
        if not student:
            return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        student_data = {
            'id': student[0],
            'name': student[1],
            'email': student[2],
            'phone': student[3],
            'age': student[4],
            'address': student[5],
            'created_at': str(student[6])
        }
        
        return jsonify({'success': True, 'student': student_data}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================== UPDATE ENDPOINTS ========================

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student"""
    try:
        data = request.get_json()
        
        # Check if student exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            cursor.close()
            return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        # Validate data (for updates)
        errors = validate_student_data(data, is_update=True)
        if errors:
            cursor.close()
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Check if new email already exists for another student
        if 'email' in data:
            cursor.execute("SELECT * FROM student WHERE email = %s AND id != %s", (data['email'], student_id))
            if cursor.fetchone():
                cursor.close()
                return jsonify({'success': False, 'error': 'Email already exists'}), 409
        
        # Build update query dynamically
        update_fields = []
        update_values = []
        
        for field in ['name', 'email', 'phone', 'age', 'address']:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field])
        
        if not update_fields:
            cursor.close()
            return jsonify({'success': False, 'error': 'No fields to update'}), 400
        
        update_values.append(student_id)
        query = f"UPDATE student SET {', '.join(update_fields)} WHERE id = %s"
        
        cursor.execute(query, tuple(update_values))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Student updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================== DELETE ENDPOINTS ========================

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    try:
        cursor = mysql.connection.cursor()
        
        # Check if student exists
        cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Student not found'}), 404
        
        # Delete student
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Student deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================== HEALTH CHECK ========================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Server is running'}), 200

# ======================== ERROR HANDLERS ========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    host = '0.0.0.0' if os.environ.get('FLASK_ENV') == 'production' else 'localhost'
    
    app.run(
        debug=debug_mode,
        host=host,
        port=port,
        threaded=True
    )
