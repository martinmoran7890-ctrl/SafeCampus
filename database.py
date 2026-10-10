import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="godisgoodallthetime",  # ← ILAGAY MO ANG TOTOONG PASSWORD MO DITO!
            database="safecampus_db"
        )
        return conn
    except Error as e:
        print(f"[DB Error] {e}")
        return None

def initialize_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="godisgoodallthetime" 
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS safecampus_db")
        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] Database 'safecampus_db' is ready")
    except Error as e:
        print(f"[Create DB Error] {e}")

if __name__ == "__main__":
    initialize_database()
