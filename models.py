import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="safecampus_db"
        )
    except:
        return None


class EmergencyContact:
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM emergency_contacts ORDER BY id")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except:
            return []


class SafetyInfo:
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM safety_information ORDER BY id DESC")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except:
            return []


class EmergencyReport:
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM emergency_reports ORDER BY id DESC")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except:
            return []

    @staticmethod
    def create(report_type, location, description, reporter_name):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO emergency_reports (report_type, location, description, reporter_name) VALUES (%s, %s, %s, %s)",
                (report_type, location, description, reporter_name)
            )
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def update_status(report_id, new_status):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE emergency_reports SET status = %s WHERE id = %s", (new_status, report_id))
            conn.commit()
            return True
        except:
            return False


class EmergencyAlert:
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM emergency_alerts ORDER BY id DESC")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except:
            return []

    @staticmethod
    def create(title, message, alert_type):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO emergency_alerts (title, message, alert_type) VALUES (%s, %s, %s)",
                (title, message, alert_type)
            )
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def delete(alert_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM emergency_alerts WHERE id = %s", (alert_id,))
            conn.commit()
            return True
        except:
            return False


class UserAuth:
    @staticmethod
    def verify(username, password):
        conn = get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except:
            return None


class UserManagement:
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, role FROM users ORDER BY id")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except:
            return []

    @staticmethod
    def add_user(username, password, role):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def delete_user(user_id):
        conn = get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return True
        except:
            return False
