import mysql.connector
import time
import random
import string

#Connecting to the db instance sql1 
db_config = {
    'user': 'root',
    'password': 'root_password',
    'host': 'sql1',
    'database': 'testdb'
}

def random_string(length=10):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def insert_data():
    """Insert random data into the 'users' table."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        name = random_string()
        email = f"{name}@example.com"
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Inserted {name}, {email}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    while True:
        insert_data()
        time.sleep(1)  # Insert every 1 second

