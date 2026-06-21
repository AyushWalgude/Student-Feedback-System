import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Ayush@1203",
    "database": "student_feedback_db"
}

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        raise ConnectionError(f"Database connection failed: {e}")

def run_query(query, params=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def verify_admin(email, password):
    result = run_query(
        "SELECT * FROM admins WHERE email=%s AND password=%s",
        (email, password), fetch=True
    )
    return result[0] if result else None

def verify_student(email, password):
    result = run_query(
        "SELECT * FROM students WHERE email=%s AND password=%s", # AND is_registered=TRUE
        (email, password), fetch=True
    )
    return result[0] if result else None
