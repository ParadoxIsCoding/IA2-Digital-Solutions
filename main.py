import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

# --- Configuration ---
DATA_FILE = "data.json"

# --- Data Persistence ---

def save_data(activities_data, students_data):
    """Save the current activities and students data to a JSON file."""
    # Convert integer keys to strings for JSON compatibility
    data_to_save = {
        "activities": {str(k): v for k, v in activities_data.items()},
        "students": {str(k): v for k, v in students_data.items()}
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data_to_save, f, indent=4)
    except IOError as e:
        messagebox.showerror("Save Error", f"Could not save data to {DATA_FILE}:\n{e}")

def load_data():
    """Load activities and students from JSON file. Return defaults if file not found or invalid."""
    if not os.path.exists(DATA_FILE):
        return get_default_activities(), get_default_students()

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        # Convert string keys back to integers after loading
        activities_loaded = {int(k): v for k, v in data.get("activities", {}).items()}
        students_loaded = {int(k): v for k, v in data.get("students", {}).items()}
        return activities_loaded, students_loaded
    except (IOError, json.JSONDecodeError, ValueError) as e:
        messagebox.showwarning("Load Error", f"Could not load data from {DATA_FILE}:\n{e}\nLoading default data.")
        # If loading fails, fall back to defaults
        return get_default_activities(), get_default_students()

# --- Default Data Definitions ---

def get_default_activities():
    """Provides a default set of extracurricular activities."""
    # Combined definition for clarity
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
activities, students = load_data()
# Note: Data is now saved only when changes are made, not necessarily on initial load.

# --- Hard-coded User Credentials (for demo purposes) ---
# In a real app, use a secure authentication method.
USERS = {
    "admin": {"password": "admin123", "role": "administrator"},
    "staff": {"password": "staff123", "role": "staff"},
    # Example student accounts linked to student IDs
    "maddi": {"password": "student123", "role": "student", "student_id": 101908},
    "laura": {"password": "student123", "role": "student", "student_id": 101920},
    "don":   {"password": "student123", "role": "student", "student_id": 136111},
    "harrison": {"password": "student123", "role": "student", "student_id": 136180},
    "jim":   {"password": "student123", "role": "student", "student_id": 136179},
    # Generic student login for testing
    "student": {"password": "student123", "role": "student", "student_id": 101908},
    # Randomly generated student login example
    "rowan":   {"password": "student123", "role": "student", "student_id": 101990}, # Matches one generated ID
}

# --- Teacher Data (used for display) ---
teachers = {
    3001: {"firstname": "John",  "surname": "Smith",   "title": "Mr", "contact": "123-456-7890"},
    3002: {"firstname": "Sarah", "surname": "Connor", "title": "Ms", "contact": "987-654-3210"}
}

# --- Utility Functions ---
def format_student_info(student_id):
    """Formats student details and enrolled activities into a readable string."""
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

# --- GUI Classes ---

# Login Window (Handles user authentication)
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Extracurricular Program")
        self.geometry("450x260") # Slightly larger for comfort
        self.resizable(False, False) # Prevent resizing

        # Use a theme and basic styling
        style = ttk.Style(self)
        style.theme_use("clam") # 'clam', 'alt', 'default', 'classic' are common options
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="black")
        style.configure("TEntry", fieldbackground="white", foreground="black")
        style.configure("TButton", padding=5) # Add some padding to buttons

        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Please Login", font=("Arial", 20, "bold")).pack(pady=15)

        # Username field
        user_frame = ttk.Frame(main_frame)
        user_frame.pack(pady=5, fill=tk.X)
        ttk.Label(user_frame, text="Username:", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        self.username_entry = ttk.Entry(user_frame, width=30)
        self.username_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.username_entry.focus() # Set focus to username field initially

        # Password field
        pass_frame = ttk.Frame(main_frame)
        pass_frame.pack(pady=5, fill=tk.X)
        ttk.Label(pass_frame, text="Password:", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        self.password_entry = ttk.Entry(pass_frame, show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        # Bind Enter key to login action for convenience
        self.password_entry.bind("<Return>", self.check_credentials)

        login_button = ttk.Button(main_frame, text="Login", command=self.check_credentials)
        # Bind Enter key on the button as well (optional redundancy)
        login_button.bind("<Return>", self.check_credentials)
        login_button.pack(pady=20)

    def check_credentials(self, event=None): # Add event parameter for key binding
        """Validate entered username and password."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user_info = USERS.get(username)

        if user_info and user_info["password"] == password:
            self.destroy() # Close login window
            # Launch main app with user's role and ID (if applicable)
            MainApplication(role=user_info["role"], student_id=user_info.get("student_id"))
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            # Clear password field after failed attempt
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus() # Keep focus on username

# Main Application Window (Container for role-specific views)
class MainApplication(tk.Tk):
    def __init__(self, role, student_id=None):
        super().__init__()
        self.role = role
        self.student_id = student_id

        self.title(f"Extracurricular Program - {role.capitalize()} View")
        self.geometry("950x600") # Adjusted size

        # Top Bar: Title and Logout
        top_frame = ttk.Frame(self, padding=(10, 5))
        top_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(top_frame, text="Extracurricular Program Management", font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        logout_btn = ttk.Button(top_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=10)

        # Main Content Area
        self.content_frame = ttk.Frame(self, padding=10)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Load the frame appropriate for the user's role
        self.load_role_frame()

        # Handle window close event to ensure data saving if needed (optional)
        # self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.mainloop()

    def load_role_frame(self):
        """Creates and displays the frame based on the user's role."""
        # Clear any existing frames first (though usually only called once)
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.role == "administrator":
            AdminFrame(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif self.role == "staff":
            StaffFrame(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif self.role == "student":
            if self.student_id:
                StudentFrame(self.content_frame, self.student_id).pack(fill=tk.BOTH, expand=True)
            else:
                messagebox.showerror("Error", "Student ID not found for student login.")
                self.logout() # Log out if student ID is missing
        else:
            messagebox.showerror("Error", f"Unknown user role: {self.role}")
            self.logout() # Log out if role is invalid

    def logout(self):
        """Log out the current user and return to the login screen."""
        # Optional: Ask for confirmation
        # if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        self.destroy()
        LoginWindow().mainloop()

    # Optional: Add handler for closing the window
    # def on_close(self):
    #     """Handle window close event."""
    #     # Could add a prompt to save unsaved changes here if needed
    #     # For now, just calls logout logic
    #     self.logout()


# Administrator View Frame
class AdminFrame(ttk.Frame):
    """Admin panel for managing activities and viewing enrollments."""
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        # Split into two main panels
        left_panel = ttk.Frame(self)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.right_panel = ttk.Frame(self, relief=tk.GROOVE, borderwidth=1) # Add border for visual separation
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        ttk.Label(left_panel, text="Activities Overview", font=("Arial", 16, "bold")).pack(anchor=tk.NW, pady=(0, 10))

        # Activities Treeview
        columns = ("activity_id", "activity", "cost", "enrollments", "income")
        self.activity_tree = ttk.Treeview(left_panel, columns=columns, show="headings", height=15)
        self.setup_treeview_columns(self.activity_tree, columns, {"cost": 60, "enrollments": 90, "income": 90})
        self.activity_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.activity_tree.bind("<<TreeviewSelect>>", self.on_activity_select)

        # Buttons below the tree
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(pady=10, fill=tk.X, anchor=tk.SW)
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_activities).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add/Edit Activity", command=self.show_activity_editor).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Activity", command=self.delete_selected_activity).pack(side=tk.LEFT, padx=5)

        # Initial message in right panel
        self.clear_right_panel("Select an activity to see details or edit.")
        self.refresh_activities() # Load initial data

    def setup_treeview_columns(self, tree, cols, widths=None):
        """Helper to configure Treeview columns."""
        widths = widths or {}
        for col in cols:
            tree.heading(col, text=col.replace("_", " ").title()) # Make headings readable
            tree.column(col, width=widths.get(col, 100), anchor=tk.W) # Default width 100

    def clear_right_panel(self, message=""):
        """Clear the right panel and optionally display a message."""
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        if message:
            ttk.Label(self.right_panel, text=message, padding=10, wraplength=300).pack(pady=20)

    def refresh_activities(self):
        """Reload and display activity data in the treeview."""
        self.activity_tree.delete(*self.activity_tree.get_children()) # Clear existing items
        sorted_activities = sorted(activities.items()) # Display sorted by ID

        for act_id, data in sorted_activities:
            cost = data.get("cost", 0)
            enroll_count = self.count_enrollments(act_id)
            income = cost * enroll_count
            self.activity_tree.insert("", tk.END, values=(act_id, data.get("activity", "N/A"), f"${cost}", enroll_count, f"${income}"))
        # Note: Removed save_data from refresh - only save when data actually changes.

    def count_enrollments(self, activity_id):
        """Count how many students are enrolled in a specific activity."""
        return sum(1 for s_data in students.values() if activity_id in s_data.get("activities_enrolled", []))

    def show_activity_editor(self, activity_id_to_edit=None):
        """Display form in the right panel to add or edit an activity."""
        self.clear_right_panel() # Clear previous content

        editor_frame = ttk.Frame(self.right_panel, padding=15)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        activity_data = activities.get(activity_id_to_edit, {}) if activity_id_to_edit else {}
        title = "Edit Activity" if activity_id_to_edit else "Add New Activity"
        ttk.Label(editor_frame, text=title, font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=tk.W)

        # Define fields to edit/add
        fields = {
            "Activity ID": {"entry": ttk.Entry(editor_frame), "value": activity_id_to_edit if activity_id_to_edit else "(New)", "row": 1, "state": tk.DISABLED if activity_id_to_edit else tk.NORMAL },
            "Activity Name": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("activity", ""), "row": 2},
            "Year Level": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("year_level", ""), "row": 3},
            "Location": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("location", ""), "row": 4},
            "Days": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("days", ""), "row": 5},
            "Time": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("time", ""), "row": 6},
            "Cost ($)": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("cost", 0), "row": 7},
            "Teacher ID": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("teacher_id", ""), "row": 8},
            "Start Date (dd/mm/yyyy)": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("start_date", ""), "row": 9},
            "End Date (dd/mm/yyyy)": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("end_date", ""), "row": 10},
        }

        entries = {} # To collect entry widgets for saving
        for i, (label, config) in enumerate(fields.items()):
            ttk.Label(editor_frame, text=f"{label}:").grid(row=config["row"], column=0, sticky=tk.W, pady=2, padx=5)
            entry = config["entry"]
            entry.grid(row=config["row"], column=1, sticky=tk.EW, pady=2, padx=5)
            entry.insert(0, config["value"])
            if "state" in config:
                entry.config(state=config["state"])
            entries[label] = entry # Store the entry widget

        editor_frame.columnconfigure(1, weight=1) # Make entry column expandable

        def save_activity():
            """Gather data from entries and save the activity."""
            act_name = entries["Activity Name"].get().strip()
            cost_str = entries["Cost ($)"].get().strip()
            teacher_id_str = entries["Teacher ID"].get().strip()

            if not act_name:
                messagebox.showerror("Error", "Activity Name is required.")
                return
            try:
                cost_val = int(cost_str) if cost_str else 0
            except ValueError:
                messagebox.showerror("Error", "Cost must be a whole number.")
                return
            try:
                teacher_id_val = int(teacher_id_str) if teacher_id_str else None
            except ValueError:
                messagebox.showerror("Error", "Teacher ID must be a number (or blank).")
                return

            # Prepare data dictionary
            updated_data = {
                "activity": act_name,
                "year_level": entries["Year Level"].get().strip(),
                "location": entries["Location"].get().strip(),
                "days": entries["Days"].get().strip(),
                "time": entries["Time"].get().strip(),
                "cost": cost_val,
                "teacher_id": teacher_id_val,
                "start_date": entries["Start Date (dd/mm/yyyy)"].get().strip(),
                "end_date": entries["End Date (dd/mm/yyyy)"].get().strip()
            }

            if activity_id_to_edit: # Editing existing
                act_id = activity_id_to_edit
                activities[act_id].update(updated_data)
                message = "Activity updated successfully."
            else: # Adding new
                # Find the next available ID
                new_id = max(activities.keys()) + 1 if activities else 2001
                activities[new_id] = updated_data
                message = "Activity added successfully."

            save_data(activities, students) # Save changes to file
            self.refresh_activities() # Update the tree view
            messagebox.showinfo("Success", message)
            self.clear_right_panel("Select an activity or Add/Edit.") # Clear form

        save_button = ttk.Button(editor_frame, text="Save Activity", command=save_activity)
        save_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

    def on_activity_select(self, event):
        """When an activity is selected, show enrolled students in the right panel."""
        selection = self.activity_tree.selection()
        if not selection:
            self.clear_right_panel("Select an activity to see enrolled students.")
            return
        item_values = self.activity_tree.item(selection[0], "values")
        if not item_values: return

        try:
            act_id = int(item_values[0])
            act_name = activities.get(act_id, {}).get("activity", "Unknown")
            self.show_enrolled_students(act_id, act_name)
        except (ValueError, IndexError):
            self.clear_right_panel("Error retrieving activity details.")

    def show_enrolled_students(self, activity_id, activity_name):
        """Display list of students enrolled in the selected activity."""
        self.clear_right_panel() # Clear previous content

        details_frame = ttk.Frame(self.right_panel, padding=15)
        details_frame.pack(fill=tk.BOTH, expand=True)

        title = f"Students in: {activity_name} (ID: {activity_id})"
        ttk.Label(details_frame, text=title, font=("Arial", 14, "bold")).pack(anchor=tk.NW, pady=(0, 10))

        columns = ("student_id", "name", "year_level", "house")
        students_tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=10)
        self.setup_treeview_columns(students_tree, columns, {"student_id": 80, "year_level": 80})
        students_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        students_tree.bind("<<TreeviewSelect>>", self.on_student_select) # Bind selection

        # Populate the tree
        enrolled_count = 0
        for s_id, s_data in students.items():
            if activity_id in s_data.get("activities_enrolled", []):
                name = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
                students_tree.insert("", tk.END, values=(s_id, name, s_data.get("year_level", 'N/A'), s_data.get("house", 'N/A')))
                enrolled_count += 1

        if enrolled_count == 0:
            ttk.Label(details_frame, text="No students currently enrolled.").pack(pady=10)

        # Add an Edit button for the selected activity below the student list
        edit_button = ttk.Button(details_frame, text=f"Edit '{activity_name}' Details", command=lambda: self.show_activity_editor(activity_id))
        edit_button.pack(pady=10, anchor=tk.SW)

        # Label to display selected student's info
        self.student_info_label_admin = ttk.Label(details_frame, text="Select a student to view details.", justify=tk.LEFT, wraplength=350)
        self.student_info_label_admin.pack(fill=tk.X, pady=10, side=tk.BOTTOM)

    def on_student_select(self, event):
        """Display details of the student selected in the enrolled list."""
        # Need the tree that triggered the event
        tree = event.widget
        selection = tree.selection()
        if not selection: return
        vals = tree.item(selection[0], "values")
        try:
            st_id = int(vals[0])
            info = format_student_info(st_id)
            self.student_info_label_admin.config(text=info)
        except (ValueError, IndexError):
            self.student_info_label_admin.config(text="Could not retrieve student details.")

    def delete_selected_activity(self):
        """Delete the activity selected in the main treeview."""
        selection = self.activity_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an activity to delete.")
            return
        item_values = self.activity_tree.item(selection[0], "values")
        try:
            act_id = int(item_values[0])
            act_name = activities.get(act_id, {}).get("activity", "this activity")
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Could not identify the selected activity.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete '{act_name}' (ID: {act_id})?\nThis will also remove it from all enrolled students."):
            # Remove the activity itself
            if act_id in activities:
                del activities[act_id]

            # Remove the activity ID from all students enrolled in it
            for s_id in list(students.keys()): # Iterate over a copy of keys for safe modification
                if act_id in students[s_id].get("activities_enrolled", []):
                    students[s_id]["activities_enrolled"].remove(act_id)

            save_data(activities, students) # Save the changes
            self.refresh_activities() # Update the tree
            self.clear_right_panel("Activity deleted. Select another activity or Add/Edit.") # Clear the right panel
            messagebox.showinfo("Deleted", f"Activity '{act_name}' has been deleted.")


# Staff View Frame
class StaffFrame(ttk.Frame):
    """Staff panel for viewing activities, enrollments, and student details."""
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        ttk.Label(self, text="Staff Dashboard", font=("Arial", 16, "bold")).pack(anchor=tk.NW, pady=(0, 10))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # --- Activities Tab ---
        self.activities_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.activities_tab, text="View Activities & Enrollments")

        # Split activities tab vertically
        act_list_frame = ttk.Frame(self.activities_tab)
        act_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.student_details_frame = ttk.Frame(self.activities_tab, relief=tk.GROOVE, borderwidth=1)
        self.student_details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Treeview for activities
        ttk.Label(act_list_frame, text="Select Activity:", font=("Arial", 12)).pack(anchor=tk.NW)
        columns_act = ("activity_id", "activity", "enrollments")
        self.act_tree = ttk.Treeview(act_list_frame, columns=columns_act, show="headings", height=10)
        self.setup_treeview_columns(self.act_tree, columns_act, {"enrollments": 100})
        self.act_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.act_tree.bind("<<TreeviewSelect>>", self.on_activity_select) # Single-click action

        # Treeview for enrolled students (within the same left frame)
        ttk.Label(act_list_frame, text="Enrolled Students:", font=("Arial", 12)).pack(anchor=tk.NW, pady=(10,0))
        cols_students = ("student_id", "name", "year_level")
        self.act_students_tree = ttk.Treeview(act_list_frame, columns=cols_students, show="headings", height=8)
        self.setup_treeview_columns(self.act_students_tree, cols_students, {"year_level": 80})
        self.act_students_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.act_students_tree.bind("<<TreeviewSelect>>", self.on_enrolled_student_select) # Single-click action

        # Refresh button for activities tab
        ttk.Button(act_list_frame, text="Refresh Lists", command=self.refresh_activities).pack(pady=10, anchor=tk.SW)

        # Display area for selected student's info (in the right frame)
        ttk.Label(self.student_details_frame, text="Student Information", font=("Arial", 14, "bold")).pack(pady=10)
        self.student_info_label_act = ttk.Label(self.student_details_frame, text="Select a student from the 'Enrolled Students' list.", justify=tk.LEFT, wraplength=350, padding=10)
        self.student_info_label_act.pack(fill=tk.BOTH, expand=True)


        # --- Students Tab ---
        self.students_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.students_tab, text="View All Students")

        # Split students tab vertically
        student_list_frame = ttk.Frame(self.students_tab)
        student_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.student_info_frame_st = ttk.Frame(self.students_tab, relief=tk.GROOVE, borderwidth=1)
        self.student_info_frame_st.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Treeview for all students
        ttk.Label(student_list_frame, text="All Students:", font=("Arial", 12)).pack(anchor=tk.NW)
        columns_st = ("student_id", "name", "year", "house", "num_activities")
        self.st_tree = ttk.Treeview(student_list_frame, columns=columns_st, show="headings", height=20)
        self.setup_treeview_columns(self.st_tree, columns_st, {"year": 60, "house": 80, "num_activities": 100})
        self.st_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.st_tree.bind("<Double-1>", self.on_student_double_click) # Double-click action

        # Refresh button for students tab
        ttk.Button(student_list_frame, text="Refresh Student List", command=self.refresh_students).pack(pady=10, anchor=tk.SW)

        # Display area for selected student's info (in the right frame)
        ttk.Label(self.student_info_frame_st, text="Student Information", font=("Arial", 14, "bold")).pack(pady=10)
        self.info_label_st = ttk.Label(self.student_info_frame_st, text="Double-click a student in the list to view details.", justify=tk.LEFT, wraplength=350, padding=10)
        self.info_label_st.pack(fill=tk.BOTH, expand=True)

        # Initial data load
        self.refresh_activities()
        self.refresh_students()

    def setup_treeview_columns(self, tree, cols, widths=None):
        """Helper to configure Treeview columns."""
        widths = widths or {}
        for col in cols:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=widths.get(col, 120), anchor=tk.W) # Default width 120

    def refresh_activities(self):
        """Reload data for the activities tree and clear student list/details."""
        # Clear activities tree
        self.act_tree.delete(*self.act_tree.get_children())
        sorted_activities = sorted(activities.items()) # Sort by ID

        # Populate activities tree
        for act_id, data in sorted_activities:
            enroll_count = sum(1 for s in students.values() if act_id in s.get("activities_enrolled", []))
            self.act_tree.insert("", tk.END, values=(act_id, data.get("activity", "N/A"), enroll_count))

        # Clear dependent views
        self.act_students_tree.delete(*self.act_students_tree.get_children())
        self.student_info_label_act.config(text="Select an activity, then a student.")
        # No save_data here - this is just reading.

    def refresh_students(self):
        """Reload data for the main student list."""
        self.st_tree.delete(*self.st_tree.get_children())
        sorted_students = sorted(students.items()) # Sort by ID

        for s_id, s_data in sorted_students:
            fullname = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
            num_act = len(s_data.get("activities_enrolled", []))
            self.st_tree.insert("", tk.END, values=(s_id, fullname, s_data.get("year_level", "N/A"), s_data.get("house", "N/A"), num_act))
        # Clear student detail view on refresh
        self.info_label_st.config(text="Double-click a student in the list.")
        # No save_data here.

    def on_activity_select(self, event):
        """Update the 'Enrolled Students' list when an activity is clicked."""
        selection = self.act_tree.selection()
        if not selection: return
        item_vals = self.act_tree.item(selection[0], "values")
        if not item_vals: return

        try:
            activity_id = int(item_vals[0])
            # Clear existing enrolled students tree
            self.act_students_tree.delete(*self.act_students_tree.get_children())
            # Clear student info panel
            self.student_info_label_act.config(text="Select a student from the list above.")

            # Populate with enrolled students
            enrolled_count = 0
            for s_id, s_data in students.items():
                if activity_id in s_data.get("activities_enrolled", []):
                    name = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
                    year = s_data.get("year_level", 'N/A')
                    self.act_students_tree.insert("", tk.END, values=(s_id, name, year))
                    enrolled_count += 1
            if enrolled_count == 0:
                 self.student_info_label_act.config(text="No students enrolled in this activity.")

        except (ValueError, IndexError):
             self.student_info_label_act.config(text="Error loading student list.")

    def on_enrolled_student_select(self, event):
        """Display details of the student selected from the 'Enrolled Students' list."""
        selection = self.act_students_tree.selection()
        if not selection: return
        vals = self.act_students_tree.item(selection[0], "values")
        try:
            student_id = int(vals[0])
            info = format_student_info(student_id)
            self.student_info_label_act.config(text=info) # Update label in the right frame
        except (ValueError, IndexError):
            self.student_info_label_act.config(text="Could not retrieve student details.")

    def on_student_double_click(self, event):
        """Display details of the student double-clicked in the main 'Students' tab."""
        selection = self.st_tree.selection()
        if not selection: return
        item_vals = self.st_tree.item(selection[0], "values")
        try:
            student_id = int(item_vals[0])
            info = format_student_info(student_id)
            self.info_label_st.config(text=info) # Update label in the right frame of students tab
        except (ValueError, IndexError):
            self.info_label_st.config(text="Could not retrieve student details.")


# Student View Frame
class StudentFrame(ttk.Frame):
    """Student panel for viewing and managing their club enrollments."""
    def __init__(self, parent, student_id):
        super().__init__(parent, padding=10)
        self.student_id = student_id
        student_name = f"{students.get(student_id, {}).get('firstname', 'Student')}" # Get student's first name for title

        title = ttk.Label(self, text=f"{student_name}'s Dashboard", font=("Arial", 16, "bold"))
        title.pack(anchor=tk.NW, pady=(0, 10))

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Panel: Notebook for clubs
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab for "My Clubs"
        self.my_clubs_tab = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(self.my_clubs_tab, text="My Clubs")
        columns = ("club_id", "club_name")
        self.my_clubs_tree = ttk.Treeview(self.my_clubs_tab, columns=columns, show="headings", height=15)
        self.setup_treeview_columns(self.my_clubs_tree, columns, {"club_id": 80})
        self.my_clubs_tree.pack(fill=tk.BOTH, expand=True)
        self.my_clubs_tree.bind("<<TreeviewSelect>>", self.on_my_club_select)

        # Tab for "Available Clubs"
        self.available_clubs_tab = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(self.available_clubs_tab, text="Available Clubs")
        self.available_clubs_tree = ttk.Treeview(self.available_clubs_tab, columns=columns, show="headings", height=15)
        self.setup_treeview_columns(self.available_clubs_tree, columns, {"club_id": 80})
        self.available_clubs_tree.pack(fill=tk.BOTH, expand=True)
        self.available_clubs_tree.bind("<<TreeviewSelect>>", self.on_available_club_select)

        # Right Panel: Club details and action button
        right_frame = ttk.Frame(main_frame, padding=10, relief=tk.GROOVE, borderwidth=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.details_label = ttk.Label(right_frame, text="Club Details", font=("Arial", 14, "bold"))
        self.details_label.pack(anchor=tk.NW)

        # Use Text widget for multi-line details, disable editing
        self.club_details_text = tk.Text(right_frame, height=12, wrap=tk.WORD, state=tk.DISABLED, relief=tk.FLAT, background=self.cget('bg')) # Match background
        self.club_details_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Action button (Join/Leave)
        self.action_button = ttk.Button(right_frame, text="Select a club", state=tk.DISABLED, command=self.perform_club_action)
        self.action_button.pack(pady=10)
        self.selected_club_id = None # Store the currently selected club ID
        self.current_action = None # Store 'join' or 'leave'

        self.refresh_tabs() # Load initial data

    def setup_treeview_columns(self, tree, cols, widths=None):
        """Helper to configure Treeview columns."""
        widths = widths or {}
        for col in cols:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=widths.get(col, 150), anchor=tk.W) # Default width 150

    def refresh_tabs(self):
        """Reload the 'My Clubs' and 'Available Clubs' lists."""
        # Clear existing items
        self.my_clubs_tree.delete(*self.my_clubs_tree.get_children())
        self.available_clubs_tree.delete(*self.available_clubs_tree.get_children())

        student_data = students.get(self.student_id, {})
        enrolled_ids = set(student_data.get("activities_enrolled", [])) # Use a set for faster lookups

        sorted_activities = sorted(activities.items()) # Sort by ID

        # Populate both trees
        for club_id, club_data in sorted_activities:
            club_name = club_data.get("activity", "Unknown Club")
            if club_id in enrolled_ids:
                self.my_clubs_tree.insert("", tk.END, values=(club_id, club_name))
            else:
                self.available_clubs_tree.insert("", tk.END, values=(club_id, club_name))

        # Clear details after refresh
        self.clear_details()

    def display_club_details(self, club_id):
        """Show details of the selected club in the text area."""
        club = activities.get(club_id)
        if not club:
            details = "Club details not found."
        else:
            details_list = [
                f"Club ID: {club_id}",
                f"Name: {club.get('activity', 'N/A')}",
                f"Year Level(s): {club.get('year_level', 'N/A')}",
                f"Location: {club.get('location', 'N/A')}",
                f"Schedule: {club.get('days', 'N/A')} at {club.get('time', 'N/A')}",
                f"Cost: ${club.get('cost', 0)}",
                f"Dates: {club.get('start_date', 'N/A')} to {club.get('end_date', 'N/A')}"
            ]
            teacher_id = club.get("teacher_id")
            if teacher_id and teacher_id in teachers:
                t_data = teachers[teacher_id]
                details_list.append(f"Teacher: {t_data.get('title','')} {t_data.get('firstname','')} {t_data.get('surname','')}")
            else:
                 details_list.append("Teacher: N/A")

            details = "\n".join(details_list)

        # Update the text widget
        self.club_details_text.config(state=tk.NORMAL) # Enable writing
        self.club_details_text.delete("1.0", tk.END) # Clear previous content
        self.club_details_text.insert(tk.END, details)
        self.club_details_text.config(state=tk.DISABLED) # Disable editing

    def update_action_button(self, club_id, action_type):
        """Configure the action button (Join/Leave)."""
        self.selected_club_id = club_id
        self.current_action = action_type
        button_text = "Leave Club" if action_type == 'leave' else "Join Club"
        self.action_button.config(text=button_text, state=tk.NORMAL)

    def on_my_club_select(self, event):
        """Handle selection in the 'My Clubs' list."""
        selection = self.my_clubs_tree.selection()
        if selection:
            # Deselect from the other tree if necessary
            self.available_clubs_tree.selection_remove(self.available_clubs_tree.selection())
            item_vals = self.my_clubs_tree.item(selection[0], "values")
            try:
                club_id = int(item_vals[0])
                self.display_club_details(club_id)
                self.update_action_button(club_id, 'leave')
            except (ValueError, IndexError):
                self.clear_details()

    def on_available_club_select(self, event):
        """Handle selection in the 'Available Clubs' list."""
        selection = self.available_clubs_tree.selection()
        if selection:
            # Deselect from the other tree if necessary
            self.my_clubs_tree.selection_remove(self.my_clubs_tree.selection())
            item_vals = self.available_clubs_tree.item(selection[0], "values")
            try:
                club_id = int(item_vals[0])
                self.display_club_details(club_id)
                self.update_action_button(club_id, 'join')
            except (ValueError, IndexError):
                self.clear_details()

    def perform_club_action(self):
        """Execute the join or leave action based on current state."""
        if not self.selected_club_id or not self.current_action:
            messagebox.showwarning("Action Error", "No club selected or action defined.")
            return

        club_id = self.selected_club_id
        action = self.current_action
        club_name = activities.get(club_id, {}).get("activity", "this club")

        student_data = students.get(self.student_id)
        if not student_data:
             messagebox.showerror("Error", "Student data not found.")
             return # Should not happen if logged in correctly

        enrolled_list = student_data.setdefault("activities_enrolled", [])

        if action == 'join':
            if club_id not in enrolled_list:
                enrolled_list.append(club_id)
                messagebox.showinfo("Success", f"You have joined '{club_name}'.")
                save_data(activities, students) # Save the change
                self.refresh_tabs() # Update UI
            else:
                messagebox.showinfo("Info", f"You are already enrolled in '{club_name}'.")
        elif action == 'leave':
            if club_id in enrolled_list:
                if messagebox.askyesno("Confirm Leave", f"Are you sure you want to leave '{club_name}'?"):
                    enrolled_list.remove(club_id)
                    messagebox.showinfo("Success", f"You have left '{club_name}'.")
                    save_data(activities, students) # Save the change
                    self.refresh_tabs() # Update UI
            else:
                 messagebox.showinfo("Info", f"You are not currently enrolled in '{club_name}'.")
        else:
            messagebox.showerror("Error", "Unknown action requested.")

    def clear_details(self):
        """Clear the details text and disable the action button."""
        self.club_details_text.config(state=tk.NORMAL)
        self.club_details_text.delete("1.0", tk.END)
        self.club_details_text.insert(tk.END, "Select a club from the lists.")
        self.club_details_text.config(state=tk.DISABLED)
        self.action_button.config(text="Select a club", state=tk.DISABLED)
        self.selected_club_id = None
        self.current_action = None
        # Ensure no selection remains visually in trees
        self.my_clubs_tree.selection_remove(self.my_clubs_tree.selection())
        self.available_clubs_tree.selection_remove(self.available_clubs_tree.selection())


# --- Main Execution ---
def main():
    """Start the application by showing the login window."""
    login_window = LoginWindow()
    login_window.mainloop()

if __name__ == "__main__":
    main()