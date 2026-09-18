from database import Database
import random
from datetime import datetime, timedelta

db = Database()
if not db.connect():
    print("❌ Hindi makakonekta sa database")
    exit()
conn = db.get_connection()
cursor = conn.cursor()

names = [
    "Campus Security Main", "Gate 1 Security Post", "Gate 2 Security Post",
    "University Health Clinic", "Office of Student Affairs", "Campus Fire Safety Unit",
    "Local Police Station", "Disaster Risk Reduction Office", "Guidance & Counseling",
    "Facilities Management", "IT Support Desk", "Women & Child Protection Unit",
    "Student Council", "Health Services", "Legal Affairs Office", "Admin Building",
    "Dormitory Management", "Library Security", "Physical Facilities", "Canteen Management"
]
numbers = [
    "0917-123-4567", "0917-234-5678", "0917-345-6789", "0917-456-7890",
    "0918-111-2222", "0918-222-3333", "0918-333-4444", "0918-444-5555",
    "0919-555-6666", "0919-666-7777", "0919-777-8888", "0919-888-9999",
    "0920-111-3333", "0920-222-4444", "0920-333-5555", "0920-444-6666",
    "0921-555-7777", "0921-666-8888", "0921-777-9999", "0921-888-0000"
]
categories_contact = ["Security", "Medical", "Admin", "Emergency", "Support"]

safety_titles = [
    "Fire Evacuation Procedure", "Earthquake Safety Protocol", "Medical Emergency Response",
    "Campus Lockdown Guidelines", "Flood Preparedness Plan", "Typhoon Response Protocol",
    "Power Outage Procedures", "Chemical Spill Response", "First Aid Basics",
    "Reporting Suspicious Activity", "Building Evacuation Map", "Assembly Points",
    "Emergency Alarm Signals", "Fire Extinguisher Usage", "Electrical Safety",
    "Crowd Control Guidelines", "Student ID & Access Policy", "After-Hours Safety",
    "Weather Advisory Channels", "Emergency Kit Checklist"
]
safety_contents = [
    "Walk calmly to nearest exit, do not use elevators, meet at designated assembly area.",
    "Drop, Cover, and Hold. Stay away from glass windows and heavy objects. Do not run.",
    "Call campus clinic immediately. Provide exact location and condition of person.",
    "Remain indoors. Lock doors. Do not open for unknown persons. Wait for all-clear signal.",
    "Move to higher ground immediately. Follow designated evacuation routes. Do not wade in floodwaters.",
    "Monitor official announcements. Prepare emergency supplies. Follow suspension notices.",
    "Report to security immediately. Use flashlights, not candles. Unplug appliances.",
    "Alert supervisor immediately. Do not touch or inhale. Follow safety data sheet instructions.",
    "Check scene is safe. Call for help. Apply pressure to bleeding wounds. Do not move injured unnecessarily.",
    "Note location, description, time. Report to security desk or use anonymous hotline.",
    "Refer to posted maps inside each room and hallway. Red lines = primary exits.",
    "Main Gym (North Field), Admin Building Parking, Engineering Field, Library Plaza.",
    "One long blast = Evacuate. Three short blasts = Alert. Continuous = All Clear.",
    "Pull pin, aim at base, squeeze handle, sweep side to side. Stand 6 meters away.",
    "Do not overload outlets. Report frayed wires. Turn off before leaving room.",
    "Follow designated flow. Do not push or run. Yield to emergency personnel.",
    "Carry ID at all times. Present when asked. Report lost ID immediately.",
    "Travel in groups. Use lighted paths. Know emergency numbers before leaving.",
    "Official Facebook page, SMS alerts, campus radio, university website.",
    "Water, flashlight, batteries, first aid kit, whistle, non-perishable food, phone charger."
]
categories_safety = ["Safety", "Protocol", "Guidelines", "Emergency", "Preparedness"]

incident_titles = [
    "Minor injury reported in Hall A", "Suspicious person near Gate 2",
    "Water leak in Admin CR", "Fallen tree branch near Gym",
    "Power outage in Engineering Bldg", "Broken light at 2nd floor hallway",
    "Small fire in cafeteria waste bin — extinguished", "Lost student ID reported",
    "Stray dog near Dormitory", "Smoke detected near Library AC room",
    "Flooding at back entrance after rain", "Door lock malfunction Room 302",
    "Medical emergency — student fainted at canteen", "Unauthorized vehicle parked at fire lane",
    "Flickering lights — 3rd floor Science", "Wet floor — no signage near stairs",
    "Missing property — laptop in lab", "Elevator stuck with 2 persons inside",
    "Overcrowding at cafeteria lunch", "Verbal dispute near parking area"
]
locations = [
    "Main Campus — Hall A", "Gate 2 Entrance", "Admin Building — CR",
    "Sports Complex — Gym", "Engineering Building — B Wing", "Science Building — 2nd Floor",
    "Main Cafeteria", "Student Dormitory — North Wing", "University Library",
    "Back Entrance Road", "Academic Building — Room 302", "Student Center — Canteen",
    "Parking Area — East", "Science Building — 3rd Floor", "Main Stairway",
    "Computer Lab — Room 405", "Admin Building — Elevator 2", "Cafeteria — Dining Hall",
    "Student Parking — West", "Quadrangle Area"
]
statuses = ["pending", "resolved", "ongoing"]

print("🔨 Deleting old data...")
cursor.execute("DELETE FROM emergency_contacts")
conn.commit()
print("✅ Cleared contacts table")

print("🔨 Inserting 50 contacts...")
for i in range(50):
    name = random.choice(names)
    num = random.choice(numbers)
    cat = random.choice(categories_contact)
    desc = f"Contact {i+1} — Available during office hours and emergencies."
    cursor.execute(
        "INSERT INTO emergency_contacts (name, contact_number, category, description) VALUES (%s, %s, %s, %s)",
        (name, num, cat, desc)
    )
conn.commit()
print("✅ 50 Emergency Contacts inserted")

print("🔨 Inserting 50 safety info...")
cursor.execute("DELETE FROM safety_info")
conn.commit()
for i in range(50):
    idx = i % len(safety_titles)
    title = safety_titles[idx] + f" — Set {i+1}"
    content = safety_contents[idx]
    cat = random.choice(categories_safety)
    cursor.execute(
        "INSERT INTO safety_info (title, content, category) VALUES (%s, %s, %s)",
        (title, content, cat)
    )
conn.commit()
print("✅ 50 Safety Info inserted")

print("🔨 Inserting 150 incidents...")
cursor.execute("DELETE FROM incidents")
conn.commit()
start_date = datetime(2026, 8, 1)
for i in range(150):
    idx = i % len(incident_titles)
    title = incident_titles[idx]
    desc = f"Incident #{i+1} — Reported case. Status updated regularly."
    loc = locations[idx]
    days = random.randint(0, 18)
    hrs = random.randint(6, 22)
    mins = random.randint(0, 59)
    rep_date = start_date + timedelta(days=days, hours=hrs, minutes=mins)
    stat = random.choice(statuses)
    cursor.execute(
        "INSERT INTO incidents (title, description, location, date_reported, status, reported_by) VALUES (%s, %s, %s, %s, %s, %s)",
        (title, desc, loc, rep_date, stat, 1)
    )
conn.commit()
print("✅ 150 Incidents inserted")

cursor.execute("SELECT COUNT(*) FROM emergency_contacts")
cnt1 = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM safety_info")
cnt2 = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM incidents")
cnt3 = cursor.fetchone()[0]
total = cnt1 + cnt2 + cnt3

print(f"\n🎉 TAPOS NA!")
print(f"   Contacts: {cnt1}")
print(f"   Safety:   {cnt2}")
print(f"   Incidents:{cnt3}")
print(f"   KABUUHAN: {total} RECORDS")

cursor.close()
conn.close()