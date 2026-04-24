import mysql.connector
from mysql.connector import Error

def insert_sample_data():
    """Insert sample student data for testing"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Change if you have a password
            database='student_db'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            sample_students = [
                ("Alice Johnson", "alice@example.com", "8765432109", 22, "789 Pine Avenue, New York"),
                ("Bob Wilson", "bob@example.com", "9876543210", 20, "456 Oak Road, Los Angeles"),
                ("Carol White", "carol@example.com", "7654321098", 21, "321 Elm Street, Chicago"),
                ("David Brown", "david@example.com", "6543210987", 23, "654 Maple Drive, Houston"),
                ("Eve Davis", "eve@example.com", "5432109876", 19, "987 Cedar Lane, Phoenix"),
            ]
            
            insert_query = """
            INSERT INTO student (name, email, phone, age, address)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_query, sample_students)
            connection.commit()
            
            print(f"✓ Successfully inserted {cursor.rowcount} sample students")
            
            # Display all students
            cursor.execute("SELECT * FROM student")
            print("\n✓ Current Students in Database:")
            print("-" * 80)
            print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Phone':<12} {'Age':<5} {'Address':<20}")
            print("-" * 80)
            
            for row in cursor.fetchall():
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<25} {row[3]:<12} {row[4]:<5} {row[5]:<20}")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    insert_sample_data()
