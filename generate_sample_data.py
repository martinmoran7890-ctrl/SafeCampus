import random
from database import get_connection, initialize_database

CATEGORIES_CONTACTS = ["Security", "Health", "Admin", "Emergency", "Maintenance"]
CATEGORIES_SAFETY = ["Guidelines", "Procedures", "Locations", "Equipment"]
INCIDENT_TYPES = ["Fire", "Accident", "Medical", "Theft", "Suspicious Activity", "Hazard"]
ALERT_LEVELS = ["Critical", "Warning", "Info"]

def create_tables():
    conn = get_connection()
    if not conn:
        print("[ERROR] No database connection")
        return False
    try:
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS emergency_contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                contact_number VARCHAR(50) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS safety_information (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                details TEXT NOT NULL
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS emergency_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                reporter_name VARCHAR(255),
                location VARCHAR(255) NOT NULL,
                incident_type VARCHAR(100) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS emergency_alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                alert_title VARCHAR(255) NOT NULL,
                alert_level VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'student'
            )
        """)
        
        conn.commit()
        print("[OK] All tables created")
        return True
    except Exception as e:
        print(f"[Error creating tables] {e}")
        return False
    finally:
        cur.close()
        conn.close()

def clear_data():
    conn = get_connection()
    if not conn: return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM emergency_contacts")
        cur.execute("DELETE FROM safety_information")
        cur.execute("DELETE FROM emergency_reports")
        cur.execute("DELETE FROM emergency_alerts")
        cur.execute("DELETE FROM users")
        conn.commit()
        print("[OK] Old data cleared")
    except Exception as e:
        print(f"[Clear Error] {e}")
    finally:
        cur.close()
        conn.close()

def insert_data():
    conn = get_connection()
    if not conn: return 0
    try:
        cur = conn.cursor()
        
        users = [
            ("admin", "admin123", "System Administrator", "admin"),
            ("staff", "staff123", "Campus Staff", "staff"),
            ("student", "student123", "Martin Student", "student")
        ]
        for u in users:
            cur.execute("INSERT INTO users (username, password, full_name, role) VALUES (%s, %s, %s, %s)", u)
        print(f"✅ Users: {len(users)}")
        
        names = ["Security Desk", "Clinic", "Fire Dept", "Admin Office", "IT Support", "Maintenance", "Police", "Counseling"]
        for i in range(80):
            name = random.choice(names) + f" — Line {i+1}"
            num = f"09{random.randint(100000000, 999999999)}"
            cat = random.choice(CATEGORIES_CONTACTS)
            desc = f"Contact {i+1} — Available during office hours and emergencies."
            cur.execute("INSERT INTO emergency_contacts (name, contact_number, category, description) VALUES (%s, %s, %s, %s)",
                       (name, num, cat, desc))
        print("✅ Emergency Contacts: 80")
        
        titles = ["Fire Exit Routes", "First Aid Locations", "Assembly Points", "Emergency Numbers", "Evacuation Plan", "Safety Equipment"]
        for i in range(60):
            title = f"{random.choice(titles)} — Guide {i+1}"
            cat = random.choice(CATEGORIES_SAFETY)
            details = f"Important safety information #{i+1}: Follow all posted signs and instructions from authorized personnel immediately during emergencies. Stay calm and assist others."
            cur.execute("INSERT INTO safety_information (title, category, details) VALUES (%s, %s, %s)",
                       (title, cat, details))
        print("✅ Safety Information: 60")
        
        locations = ["Main Building", "Science Bldg", "Library", "Gymnasium", "Canteen", "Dormitory", "Parking Area", "Admin Bldg"]
        statuses = ["Pending", "Processing", "Resolved"]
        for i in range(80):
            loc = random.choice(locations) + f", Room {random.randint(100, 500)}"
            typ = random.choice(INCIDENT_TYPES)
            desc = f"Reported incident: {typ.lower()} observed at {loc}. Please attend promptly."
            status = random.choice(statuses)
            reporter = random.choice(["Martin Student", "Campus Staff", "System Admin", ""])
            cur.execute("INSERT INTO emergency_reports (reporter_name, location, incident_type, description, status) VALUES (%s, %s, %s, %s, %s)",
                       (reporter, loc, typ, desc, status))
        print("✅ Incident Reports: 80")
        
        alert_titles = ["Building Inspection", "Weather Advisory", "Scheduled Drill", "Road Closure", "System Update"]
        for i in range(30):
            title = f"{random.choice(alert_titles)} — Alert {i+1}"
            level = random.choice(ALERT_LEVELS)
            msg = f"This is a {level.lower()} alert: {title}. Please take necessary precautions and remain alert."
            cur.execute("INSERT INTO emergency_alerts (alert_title, alert_level, message) VALUES (%s, %s, %s)",
                       (title, level, msg))
        print("✅ Emergency Alerts: 30")
        
        conn.commit()
        return 253
    except Exception as e:
        print(f"[Insert Error] {e}")
        return 0
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    initialize_database()
    if not create_tables():
        exit(1)
    clear_data()
    total = insert_data()
    print(f"\n✅ TOTAL RECORDS: {total}")
