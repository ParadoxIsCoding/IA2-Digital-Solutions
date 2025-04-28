import tkinter as tk
from tkinter import messagebox
import json
import os
import random

# --- Configuration ---
DATA_FILE = "data.json"

# --- Data Persistence ---

def save_data(activities_data, students_data, users_data, teachers_data):
    """Save the current activities, students, users, and teachers data to a JSON file."""
    data_to_save = {
        "activities": {str(k): v for k, v in activities_data.items()},
        "students": {str(k): v for k, v in students_data.items()},
        "users": users_data, # Usernames are already strings
        "teachers": {str(k): v for k, v in teachers_data.items()} # Convert teacher IDs to strings
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data_to_save, f, indent=4)
    except IOError as e:
        messagebox.showerror("Save Error", f"Could not save data to {DATA_FILE}:\n{e}")

def load_data():
    """Load data from JSON file. Return defaults/empty if file not found, invalid, or missing keys."""
    if not os.path.exists(DATA_FILE):
        messagebox.showwarning("Load Warning", f"{DATA_FILE} not found. Loading default activities/students. User/teacher data might be missing.")
        # Return defaults for activities/students, empty for users/teachers
        return get_default_activities(), get_default_students(), {}, {}

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # Load activities (convert keys to int), fallback to default if missing/error
        try:
            activities_loaded = {int(k): v for k, v in data.get("activities", {}).items()}
        except (ValueError, AttributeError):
             messagebox.showwarning("Load Warning", "Error reading activities data. Loading defaults.")
             activities_loaded = get_default_activities()

        # Load students (convert keys to int), fallback to default if missing/error
        try:
            students_loaded = {int(k): v for k, v in data.get("students", {}).items()}
            # Ensure activities_enrolled is a list
            for s_id, s_data in students_loaded.items():
                if "activities_enrolled" not in s_data:
                    s_data["activities_enrolled"] = []
                elif not isinstance(s_data["activities_enrolled"], list):
                    s_data["activities_enrolled"] = [] # Reset if not a list
        except (ValueError, AttributeError):
             messagebox.showwarning("Load Warning", "Error reading students data. Loading defaults.")
             students_loaded = get_default_students()

        # Load users (usernames are strings), fallback to empty if missing
        users_loaded = data.get("users", {})
        if not users_loaded:
             messagebox.showwarning("Load Warning", "User data missing from data.json. Login might fail.")

        # Load teachers (convert keys to int), fallback to empty if missing
        try:
            teachers_loaded = {int(k): v for k, v in data.get("teachers", {}).items()}
            if not teachers_loaded:
                messagebox.showwarning("Load Warning", "Teacher data missing from data.json. Teacher info might be unavailable.")
        except (ValueError, AttributeError):
             messagebox.showwarning("Load Warning", "Error reading teachers data. Teacher info might be unavailable.")
             teachers_loaded = {}


        return activities_loaded, students_loaded, users_loaded, teachers_loaded

    except (IOError, json.JSONDecodeError) as e:
        messagebox.showwarning("Load Error", f"Could not load or parse {DATA_FILE}:\n{e}\nLoading default activities/students. User/teacher data might be missing.")
        # If loading fails completely, fall back to defaults/empty
        return get_default_activities(), get_default_students(), {}, {}

# --- Default Data Definitions (Fallback only) ---

def get_default_activities():
    """Provides a default set of extracurricular activities."""
    # This function remains as the fallback if data.json is missing/corrupt
    activities = {
        # Original 7
        2001: {"activity": "Basketball", "year_level": "9-10", "location": "Gym A", "days": "Mon, Wed", "time": "3:30 PM - 4:30 PM", "cost": 40, "teacher_id": 3001, "start_date": "01/02/2025", "end_date": "30/11/2025"},
        2002: {"activity": "Chess Club", "year_level": "7-12", "location": "Room 10", "days": "Tue, Thu", "time": "3:00 PM - 4:00 PM", "cost": 20, "teacher_id": 3002, "start_date": "15/02/2025", "end_date": "01/12/2025"},
        2003: {"activity": "Soccer", "year_level": "8-10", "location": "Field", "days": "Tue, Thu", "time": "4:00 PM - 5:00 PM", "cost": 30, "teacher_id": 3001, "start_date": "01/03/2025", "end_date": "30/11/2025"},
        2004: {"activity": "Art Club", "year_level": "7-12", "location": "Art Room", "days": "Mon, Wed", "time": "3:00 PM - 4:00 PM", "cost": 25, "teacher_id": 3002, "start_date": "01/03/2025", "end_date": "30/11/2025"},
        2005: {"activity": "Drama Club", "year_level": "9-12", "location": "Auditorium", "days": "Fri", "time": "2:00 PM - 4:00 PM", "cost": 35, "teacher_id": 3002, "start_date": "01/03/2025", "end_date": "30/11/2025"},
        2006: {"activity": "Debate Club", "year_level": "10-12", "location": "Room 15", "days": "Tue", "time": "3:30 PM - 4:30 PM", "cost": 20, "teacher_id": 3001, "start_date": "01/03/2025", "end_date": "30/11/2025"},
        2007: {"activity": "Science Club", "year_level": "7-12", "location": "Lab", "days": "Thu", "time": "3:30 PM - 5:00 PM", "cost": 50, "teacher_id": 3001, "start_date": "01/03/2025", "end_date": "30/11/2025"},
        # Additional 10
        2008: {"activity": "Music Club", "year_level": "7-12", "location": "Music Room", "days": "Mon, Wed", "time": "4:00 PM - 5:00 PM", "cost": 30, "teacher_id": 3002, "start_date": "05/03/2025", "end_date": "25/11/2025"},
        2009: {"activity": "Robotics Club", "year_level": "9-12", "location": "Lab 2", "days": "Tue, Thu", "time": "4:30 PM - 5:30 PM", "cost": 45, "teacher_id": 3001, "start_date": "10/03/2025", "end_date": "20/11/2025"},
        2010: {"activity": "Dance Club", "year_level": "7-12", "location": "Dance Studio", "days": "Wed, Fri", "time": "3:30 PM - 4:30 PM", "cost": 25, "teacher_id": 3002, "start_date": "12/03/2025", "end_date": "22/11/2025"},
        2011: {"activity": "Literature Club", "year_level": "8-12", "location": "Library", "days": "Mon, Thu", "time": "4:00 PM - 5:00 PM", "cost": 15, "teacher_id": 3002, "start_date": "15/03/2025", "end_date": "28/11/2025"},
        2012: {"activity": "Coding Club", "year_level": "9-12", "location": "Computer Lab", "days": "Tue, Fri", "time": "3:30 PM - 5:00 PM", "cost": 40, "teacher_id": 3001, "start_date": "18/03/2025", "end_date": "30/11/2025"},
        2013: {"activity": "Photography Club", "year_level": "7-12", "location": "Art Room", "days": "Wed", "time": "3:00 PM - 4:30 PM", "cost": 20, "teacher_id": 3002, "start_date": "20/03/2025", "end_date": "25/11/2025"},
        2014: {"activity": "Environmental Club", "year_level": "7-12", "location": "Outdoor Garden", "days": "Thu", "time": "4:00 PM - 5:00 PM", "cost": 10, "teacher_id": 3001, "start_date": "22/03/2025", "end_date": "27/11/2025"},
        2015: {"activity": "Cooking Club", "year_level": "8-12", "location": "Kitchen", "days": "Fri", "time": "3:00 PM - 5:00 PM", "cost": 35, "teacher_id": 3002, "start_date": "25/03/2025", "end_date": "30/11/2025"},
        2016: {"activity": "Martial Arts Club", "year_level": "9-12", "location": "Gym B", "days": "Mon, Wed", "time": "4:00 PM - 5:00 PM", "cost": 50, "teacher_id": 3001, "start_date": "28/03/2025", "end_date": "30/11/2025"},
        2017: {"activity": "Gardening Club", "year_level": "7-12", "location": "School Garden", "days": "Tue", "time": "3:00 PM - 4:00 PM", "cost": 15, "teacher_id": 3002, "start_date": "30/03/2025", "end_date": "30/11/2025"}
    }
    return activities

def get_default_students():
    """Provides a default set of students with some random generation."""
    # This function remains as the fallback if data.json is missing/corrupt
    default_students = {
        # Base students
        101908: {"firstname": "Maddi", "surname": "Gascar", "gender": "Female", "year_level": 9, "house": "Bradman", "dob": "27/06/2005", "activities_enrolled": [2001]},
        101920: {"firstname": "Laura", "surname": "Norder", "gender": "Female", "year_level": 11, "house": "Chisholm", "dob": "31/07/2002", "activities_enrolled": [2002]},
        136111: {"firstname": "Don", "surname": "Keigh", "gender": "Male", "year_level": 12, "house": "Lawson", "dob": "14/06/2003", "activities_enrolled": [2002]},
        136179: {"firstname": "Jim", "surname": "Pansey", "gender": "Male", "year_level": 12, "house": "Sturt", "dob": "06/10/2002", "activities_enrolled": []},
        136180: {"firstname": "Harrison", "surname": "Chapman", "gender": "Non-Binary", "year_level": 12, "house": "Lawson", "dob": "14/06/2003", "activities_enrolled": [2002, 2001]}
    }

    # Data for random generation
    HOUSES = ["Bradman", "Chisholm", "Lawson", "Sturt"]
    FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Cameron", "Avery", "Reese", "Quinn", "Peyton", "Skyler", "Dakota", "Rowan", "Harper", "Sage", "Blake", "Drew", "Emerson"]
    SURNAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White"]
    ALL_CLUB_IDS = list(get_default_activities().keys()) # Get current club IDs

    # Generate additional students
    for student_id in range(101921, 101991): # Combined range for 70 students
        default_students[student_id] = {
            "firstname": random.choice(FIRST_NAMES),
            "surname": random.choice(SURNAMES),
            "gender": random.choice(["Male", "Female", "Non-Binary"]),
            "year_level": random.randint(7, 12),
            "house": random.choice(HOUSES),
            "dob": f"{random.randint(1,28):02}/{random.randint(1,12):02}/{random.randint(2000, 2007)}", # Adjusted year range slightly
            "activities_enrolled": [random.choice(ALL_CLUB_IDS)] # Assign one random club initially
        }
    return default_students

# --- Initial Data Load ---
# Load all data structures from the JSON file into module-level globals
# These will be imported by other modules
activities, students, USERS, teachers = load_data()


# --- Utility Functions ---
def format_student_info(student_id):
    """Formats student details and enrolled activities into a readable string."""
    # Access the global 'students' and 'activities' dictionaries
    s_data = students.get(student_id)
    if not s_data:
        return "Student not found."

    enrolled_ids = s_data.get("activities_enrolled", [])
    if enrolled_ids:
        # Get names and costs, handling cases where an activity might have been deleted
        act_names = [activities[a_id]["activity"] for a_id in enrolled_ids if a_id in activities]
        total_cost = sum(activities[a_id]["cost"] for a_id in enrolled_ids if a_id in activities)
        activities_str = ", ".join(act_names) if act_names else "None"
    else:
        activities_str = "None"
        total_cost = 0

    info = (
        f"Name: {s_data.get('firstname', 'N/A')} {s_data.get('surname', 'N/A')}\n"
        f"Gender: {s_data.get('gender', 'N/A')}\n"
        f"Year Level: {s_data.get('year_level', 'N/A')}\n"
        f"House: {s_data.get('house', 'N/A')}\n"
        f"DOB: {s_data.get('dob', 'N/A')}\n"
        f"Activities Enrolled: {activities_str}\n"
        f"Total Cost: ${total_cost}\n"
    )
    return info