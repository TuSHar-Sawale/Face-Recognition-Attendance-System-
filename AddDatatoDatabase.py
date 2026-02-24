
from supabase import create_client

SUPABASE_URL = "https://ksfqvefeqhrnqutnkpxo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzZnF2ZWZlcWhybnF1dG5rcHhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc2Mzc0MjYsImV4cCI6MjA2MzIxMzQyNn0.nylC--UMAYovLgXa5BsxHwY9_8i4Pa9C6xZ7H8bOYDU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

data = [
    {"id": "321654", "name": "Murtaza Hassan", "major": "Robotics", "starting_year": 2017, "total_attendance": 7, "standing": "G", "year": 4, "last_attendance_time": "2022-12-11 00:54:34"},
    {"id": "852741", "name": "Emly Blunt", "major": "Economics", "starting_year": 2021, "total_attendance": 12, "standing": "B", "year": 1, "last_attendance_time": "2022-12-11 00:54:34"},
    {"id": "963852", "name": "Elon Musk", "major": "Physics", "starting_year": 2020, "total_attendance": 7, "standing": "G", "year": 2, "last_attendance_time": "2022-12-11 00:54:34"},
    {"id": "1234", "name": "Tushar Sawale", "major": "Computer Science", "starting_year": 2025, "total_attendance": 7, "standing": "G", "year": 2, "last_attendance_time": "2022-12-11 00:54:34"}
]

for student in data:
    supabase.table("Students").insert(student).execute()

print("Data Inserted")
