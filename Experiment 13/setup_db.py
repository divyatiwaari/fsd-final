import mysql.connector
from mysql.connector import Error

def create_database_and_table():
    """Create database and student table"""
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Change if you have a password
            port=3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
            print("✓ Database 'student_db' created successfully")
            
            # Select database
            cursor.execute("USE student_db")
            
            # Create student table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(10) NOT NULL,
                age INT NOT NULL CHECK (age >= 18 AND age <= 60),
                address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            print("✓ Table 'student' created successfully")
            
            # Display table structure
            cursor.execute("DESCRIBE student")
            print("\n✓ Table Structure:")
            print("-" * 60)
            for row in cursor.fetchall():
                print(row)
            
            cursor.close()
            connection.close()
            print("\n✓ Database setup completed successfully!")
            
    except Error as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    create_database_and_table()
