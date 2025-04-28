# Import the json library to work with JSON data (reading from and writing to data.json).
import json
# Import the tkinter library, specifically the messagebox module for showing pop-up messages.
from tkinter import messagebox

# Define the path to the JSON file where all application data is stored.
DATA_FILE = "data.json"

# --- Global Data Dictionaries ---
# These dictionaries will hold the application's data after it's loaded from the JSON file.
# They are initialized as empty dictionaries.

# activities: Stores information about each activity (e.g., name, cost, location).
# Key: activity_id (integer), Value: dictionary of activity details.
activities = {}

# students: Stores information about each student (e.g., name, year level, enrolled activities).
# Key: student_id (integer), Value: dictionary of student details.
students = {}

# USERS: Stores login credentials for all users (students, staff, admin).
# Key: username (string, typically the user ID), Value: dictionary containing 'password' and 'role'.
USERS = {}

# teachers: Stores information about each teacher (e.g., name, contact details).
# Key: teacher_id (integer), Value: dictionary of teacher details.
teachers = {}

# --- Data Loading Function ---

def load_data():
    """Loads data from the JSON file into the global dictionaries."""
    # Use 'global' keyword to indicate that we want to modify the global variables defined above,
    # not create new local variables with the same names.
    global activities, students, USERS, teachers
    try:
        # Open the JSON file specified by DATA_FILE in read mode ('r').
        # 'with open(...)' ensures the file is automatically closed even if errors occur.
        with open(DATA_FILE, 'r') as f:
            # Load the entire JSON structure from the file.
            data = json.load(f)

            # --- Data Conversion and Population ---
            # The JSON standard only supports string keys. Our application often uses integer IDs
            # (like student_id, activity_id, teacher_id) as keys in dictionaries for easier lookups.
            # Therefore, we need to convert the string keys loaded from JSON back into integers
            # where appropriate when populating our global dictionaries.

            # Convert string keys from 'activities' in JSON to integer keys for the global 'activities' dict.
            # dict.items() gets key-value pairs. int(k) converts the string key 'k' to an integer.
            activities = {int(k): v for k, v in data.get('activities', {}).items()}

            # Convert string keys from 'students' in JSON to integer keys for the global 'students' dict.
            students = {int(k): v for k, v in data.get('students', {}).items()}

            # The 'USERS' dictionary uses usernames (strings) as keys, so no key conversion is needed.
            # Just assign the loaded 'users' data (or an empty dict if 'users' key is missing).
            USERS = data.get('users', {})

            # Convert string keys from 'teachers' in JSON to integer keys for the global 'teachers' dict.
            teachers = {int(k): v for k, v in data.get('teachers', {}).items()}

    # --- Error Handling --- 
    except FileNotFoundError:
        # If the data.json file doesn't exist, show an error message.
        messagebox.showerror("Error", f"Data file '{DATA_FILE}' not found. Cannot load data.")
        # Exit the application because it cannot function without data.
        # Consider creating a default empty file here instead of exiting in a real application.
        exit()
    except json.JSONDecodeError:
        # If the file exists but contains invalid JSON, show an error.
        messagebox.showerror("Error", f"Error decoding JSON from '{DATA_FILE}'. Check the file format.")
        # Exit the application.
        exit()
    except Exception as e:
        # Catch any other unexpected errors during loading.
        messagebox.showerror("Error", f"An unexpected error occurred while loading data: {e}")
        # Exit the application.
        exit()

# --- Data Saving Function ---

def save_data(activities_data, students_data, users_data, teachers_data):
    """Saves the current state of the data dictionaries back to the JSON file."""
    try:
        # Open the JSON file in write mode ('w'). This will overwrite the existing file.
        with open(DATA_FILE, 'w') as f:
            # Prepare the data structure to be saved. Combine all dictionaries into one main dictionary.
            # Note: JSON requires keys to be strings. Python dictionary keys (like integer IDs)
            # will be automatically converted to strings by json.dump(). When loading, we convert them back.
            data_to_save = {
                'activities': activities_data,
                'students': students_data,
                'users': users_data,
                'teachers': teachers_data
            }
            # Write the data_to_save dictionary to the file 'f'.
            # 'indent=4' makes the JSON file human-readable with pretty-printing (4 spaces indentation).
            json.dump(data_to_save, f, indent=4)
    except Exception as e:
        # If any error occurs during saving (e.g., file permissions), show an error message.
        messagebox.showerror("Save Error", f"Failed to save data to '{DATA_FILE}': {e}")

# --- Helper Function --- 

def format_student_info(student_id):
    """Formats student information into a readable string."""
    # Access the global 'students' dictionary.
    # Use .get(student_id, {}) to safely retrieve the student's data.
    # If the student_id doesn't exist, it returns an empty dictionary, preventing errors.
    student_data = students.get(student_id, {})
    # If student_data is empty (student not found), return a default message.
    if not student_data:
        return f"Student ID {student_id} not found."

    # Construct the formatted string using f-strings.
    # Use .get(key, 'N/A') for each piece of information to handle cases where a key might be missing
    # in a particular student's data, displaying 'N/A' instead of causing an error.
    info = (
        f"Name: {student_data.get('firstname', 'N/A')} {student_data.get('surname', 'N/A')}\n"
        f"Year Level: {student_data.get('year_level', 'N/A')}\n"
        f"House: {student_data.get('house', 'N/A')}\n"
        f"Email: {student_data.get('email', 'N/A')}\n"
        f"Contact: {student_data.get('contact_number', 'N/A')}"
    )
    # Return the formatted string.
    return info

# --- Initial Data Load ---
# Call load_data() immediately when this module (common.py) is imported.
# This ensures that the global dictionaries (activities, students, USERS, teachers)
# are populated with data as soon as the application starts using this module.
load_data()