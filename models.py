from database import Database

class Auth:
    def __init__(self):
        self.db = Database()
        if not self.db.connect():
            print("❌ Auth: Hindi makakonekta sa DB")

    def login(self, username, password):
        conn = self.db.get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, role, full_name FROM users WHERE username=%s AND password=%s", 
                         (username, password))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return {"id": row[0], "username": row[1], "role": row[2], "name": row[3]}
        except Exception as e:
            print(f"❌ Login Error: {e}")
        return None


class ContactManager:
    def __init__(self):
        self.db = Database()
        self.db.connect()

    def get_all(self):
        conn = self.db.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM emergency_contacts")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Contacts Error: {e}")
            return []


class SafetyManager:
    def __init__(self):
        self.db = Database()
        self.db.connect()

    def get_all(self):
        conn = self.db.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM safety_info")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Safety Error: {e}")
            return []


class IncidentManager:
    def __init__(self):
        self.db = Database()
        self.db.connect()

    def get_all(self):
        conn = self.db.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM incidents ORDER BY date_reported DESC")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Incidents Error: {e}")
            return []