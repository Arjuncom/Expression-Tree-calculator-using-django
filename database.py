# database.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="k@rthikey123",  # your MySQL password
        database="expression_db"
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expressions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            expression TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(expression, result):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eexpressions (expression, result) VALUES (%s, %s)", (expression, result))
    conn.commit()
    conn.close()
