import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "safecampus_db"
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                self.connection.database = self.database
                return True
        except Error as e:
            print(f"❌ Connection Error: {e}")
            return False

    def create_tables(self):
        cursor = self.connection.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin','student') DEFAULT 'student',
            full_name VARCHAR(100)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_contacts (
            contact_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            contact_number VARCHAR(30) NOT NULL,
            category VARCHAR(50),
            description TEXT
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS safety_info (
            info_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            category VARCHAR(50)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            location VARCHAR(150),
            date_reported DATETIME DEFAULT CURRENT_TIMESTAMP,
            status ENUM('pending','resolved','ongoing') DEFAULT 'pending',
            reported_by INT,
            FOREIGN KEY (reported_by) REFERENCES users(user_id)
        )""")

        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO users (username, password, role, full_name)
            VALUES (%s, %s, %s, %s)
            """, ("admin", "admin123", "admin", "System Administrator"))
        
        self.connection.commit()
        cursor.close()

    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection

if __name__ == "__main__":
    db = Database()
    if db.connect():
        db.create_tables()
        print("✅ Database & Tables Created Successfully!")