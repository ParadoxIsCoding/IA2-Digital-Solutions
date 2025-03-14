import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

# -------------------------------------------------------------------
# Data persistence functions
# -------------------------------------------------------------------
DATA_FILE = "data.json"

def save_data(activities_data, students_data):
    """Save activities and students to a JSON file."""
    data_to_save = {
        "activities": {str(k): v for k, v in activities_data.items()},
        "students": {str(k): v for k, v in students_data.items()}
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data_to_save, f, indent=4)

def load_data():
    """Load activities and students from JSON file. If not found, return default data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        activities_loaded = {int(k): v for k, v in data.get("activities", {}).items()}
        students_loaded = {int(k): v for k, v in data.get("students", {}).items()}
        return activities_loaded, students_loaded
    else:
        return get_default_activities(), get_default_students()

# -------------------------------------------------------------------
# Default Data Definitions
# -------------------------------------------------------------------
def get_default_activities():
    """Returns the default activities (7 total)."""
    return {
        2001: {
            "activity": "Basketball",
            "year_level": "9-10",
            "location": "Gym A",
            "days": "Mon, Wed",
            "time": "3:30 PM - 4:30 PM",
            "cost": 40,
            "teacher_id": 3001,
            "start_date": "01/02/2025",
            "end_date": "30/11/2025"
        },
        2002: {
            "activity": "Chess Club",
            "year_level": "7-12",
            "location": "Room 10",
            "days": "Tue, Thu",
            "time": "3:00 PM - 4:00 PM",
            "cost": 20,
            "teacher_id": 3002,
            "start_date": "15/02/2025",
            "end_date": "01/12/2025"
        },
        2003: {
            "activity": "Soccer",
            "year_level": "8-10",
            "location": "Field",
            "days": "Tue, Thu",
            "time": "4:00 PM - 5:00 PM",
            "cost": 30,
            "teacher_id": 3001,
            "start_date": "01/03/2025",
            "end_date": "30/11/2025"
        },
        2004: {
            "activity": "Art Club",
            "year_level": "7-12",
            "location": "Art Room",
            "days": "Mon, Wed",
            "time": "3:00 PM - 4:00 PM",
            "cost": 25,
            "teacher_id": 3002,
            "start_date": "01/03/2025",
            "end_date": "30/11/2025"
        },
        2005: {
            "activity": "Drama Club",
            "year_level": "9-12",
            "location": "Auditorium",
            "days": "Fri",
            "time": "2:00 PM - 4:00 PM",
            "cost": 35,
            "teacher_id": 3002,
            "start_date": "01/03/2025",
            "end_date": "30/11/2025"
        },
        2006: {
            "activity": "Debate Club",
            "year_level": "10-12",
            "location": "Room 15",
            "days": "Tue",
            "time": "3:30 PM - 4:30 PM",
            "cost": 20,
            "teacher_id": 3001,
            "start_date": "01/03/2025",
            "end_date": "30/11/2025"
        },
        2007: {
            "activity": "Science Club",
            "year_level": "7-12",
            "location": "Lab",
            "days": "Thu",
            "time": "3:30 PM - 5:00 PM",
            "cost": 50,
            "teacher_id": 3001,
            "start_date": "01/03/2025",
            "end_date": "30/11/2025"
        }
    }

def get_default_students():
    """Returns the default students (5 original + 20 extra)."""
    default_students = {
        101908: {
            "firstname": "Maddi",
            "surname": "Gascar",
            "gender": "Female",
            "year_level": 9,
            "house": "Bradman",
            "dob": "27/06/2005",
            "activities_enrolled": [2001]
        },
        101920: {
            "firstname": "Laura",
            "surname": "Norder",
            "gender": "Female",
            "year_level": 11,
            "house": "Chisholm",
            "dob": "31/07/2002",
            "activities_enrolled": [2002]
        },
        136111: {
            "firstname": "Don",
            "surname": "Keigh",
            "gender": "Male",
            "year_level": 12,
            "house": "Lawson",
            "dob": "14/06/2003",
            "activities_enrolled": [2002]
        },
        136179: {
            "firstname": "Jim",
            "surname": "Pansey",
            "gender": "Male",
            "year_level": 12,
            "house": "Sturt",
            "dob": "06/10/2002",
            "activities_enrolled": []
        },
        136180: {
            "firstname": "Harrison",
            "surname": "Chapman",
            "gender": "Non-Binary",
            "year_level": 12,
            "house": "Lawson",
            "dob": "14/06/2003",
            "activities_enrolled": [2002, 2001]
        }
    }

    houses = ["Bradman", "Chisholm", "Lawson", "Sturt"]
    first_names = [
        "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley",
        "Jamie", "Cameron", "Avery", "Reese", "Quinn", "Peyton",
        "Skyler", "Dakota", "Rowan", "Harper", "Sage", "Blake",
        "Drew", "Emerson"
    ]
    surnames = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller",
        "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson",
        "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson",
        "Thompson", "White"
    ]
    # Generate 20 additional students with IDs 101921 to 101940
    for student_id in range(101921, 101941):
        first = random.choice(first_names)
        last = random.choice(surnames)
        gender = random.choice(["Male", "Female", "Non-Binary"])
        year_level = random.randint(7, 12)
        house = random.choice(houses)
        dob = f"{random.randint(1,28):02}/{random.randint(1,12):02}/{2000+random.randint(0,5)}"
        activity = random.choice(list(get_default_activities().keys()))
        default_students[student_id] = {
            "firstname": first,
            "surname": last,
            "gender": gender,
            "year_level": year_level,
            "house": house,
            "dob": dob,
            "activities_enrolled": [activity]
        }
    return default_students

# -------------------------------------------------------------------
# Load or create data file
# -------------------------------------------------------------------
activities, students = load_data()
if not os.path.exists(DATA_FILE):
    save_data(activities, students)

# -------------------------------------------------------------------
# Hard-coded user credentials
# -------------------------------------------------------------------
USERS = {
    "admin": {"password": "admin123", "role": "administrator"},
    "staff": {"password": "staff123", "role": "staff"},
    "maddi": {"password": "student123", "role": "student", "student_id": 101908},
    "laura": {"password": "student123", "role": "student", "student_id": 101920},
    "don":   {"password": "student123", "role": "student", "student_id": 136111},
    "jim":   {"password": "student123", "role": "student", "student_id": 136179},
    "Harrison": {"password": "student123", "role": "student", "student_id": 136180}
}

# -------------------------------------------------------------------
# Teacher data (for reference in activity details)
# -------------------------------------------------------------------
teachers = {
    3001: {"firstname": "John",  "surname": "Smith",   "title": "Mr", "contact": "123-456-7890"},
    3002: {"firstname": "Sarah", "surname": "Connor", "title": "Ms", "contact": "987-654-3210"}
}

# -------------------------------------------------------------------
# Utility function for formatting student info
# -------------------------------------------------------------------
def format_student_info(student_id):
    s_data = students.get(student_id)
    if not s_data:
        return "Student not found."
    enrolled = s_data.get("activities_enrolled", [])
    if enrolled:
        act_names = [activities[a_id]["activity"] for a_id in enrolled if a_id in activities]
        activities_str = ", ".join(act_names)
    else:
        activities_str = "None"

    info = (
        f"Name: {s_data['firstname']} {s_data['surname']}\n"
        f"Gender: {s_data['gender']}\n"
        f"Year Level: {s_data['year_level']}\n"
        f"House: {s_data['house']}\n"
        f"DOB: {s_data['dob']}\n"
        f"Activities Enrolled: {activities_str}\n"
    )
    return info

# -------------------------------------------------------------------
# Login Window (with improved layout)
# -------------------------------------------------------------------
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Extracurricular Program")
        # Slightly bigger geometry so everything fits nicely
        self.geometry("380x220")
        self.resizable(False, False)

        # Optional: set a style for better visibility on dark mode
        style = ttk.Style(self)
        style.theme_use("default")
        # Force a light background on the main widgets (if needed)
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="black")
        style.configure("TEntry", fieldbackground="white", foreground="black")
        style.configure("TButton", background="#e0e0e0", foreground="black")

        main_frame = ttk.Frame(self, padding=20)
        # Fill both directions so the frame expands to the window size
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(main_frame, text="Please Login", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        ttk.Label(main_frame, text="Username:").pack(anchor=tk.W, pady=2)
        self.username_entry = ttk.Entry(main_frame, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(main_frame, text="Password:").pack(anchor=tk.W, pady=2)
        self.password_entry = ttk.Entry(main_frame, show="*", width=30)
        self.password_entry.pack(pady=5)

        login_button = ttk.Button(main_frame, text="Login", command=self.check_credentials)
        login_button.pack(pady=10)

    def check_credentials(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user_info = USERS.get(username)

        if user_info and user_info["password"] == password:
            self.destroy()
            MainApplication(role=user_info["role"], student_id=user_info.get("student_id"))
        else:
            messagebox.showerror("Error", "Invalid username or password")

# -------------------------------------------------------------------
# Main Application Window
# -------------------------------------------------------------------
class MainApplication(tk.Tk):
    def __init__(self, role, student_id=None):
        super().__init__()
        self.title("Extracurricular Program")
        self.geometry("900x550")
        self.role = role
        self.student_id = student_id

        # Top bar with logout
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top_frame, text="Extracurricular Program", font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        logout_btn = ttk.Button(top_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=10, pady=5)

        # Content area for role-specific frames
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Instantiate role-specific frames
        self.admin_frame = AdminFrame(self.content_frame)
        self.staff_frame = StaffFrame(self.content_frame)
        self.student_frame = StudentFrame(self.content_frame, self.student_id)

        self.show_relevant_frame()
        self.mainloop()

    def show_relevant_frame(self):
        self.admin_frame.pack_forget()
        self.staff_frame.pack_forget()
        self.student_frame.pack_forget()

        if self.role == "administrator":
            self.admin_frame.pack(fill=tk.BOTH, expand=True)
        elif self.role == "staff":
            self.staff_frame.pack(fill=tk.BOTH, expand=True)
        elif self.role == "student":
            self.student_frame.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showerror("Error", f"Unknown role: {self.role}")
            self.destroy()

    def logout(self):
        self.destroy()
        LoginWindow().mainloop()

# -------------------------------------------------------------------
# Admin Frame
# -------------------------------------------------------------------
class AdminFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.left_frame = ttk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(self, relief=tk.RIDGE)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        ttk.Label(self.left_frame, text="Administrator Panel", font=("Arial", 16, "bold")).pack(anchor=tk.N, pady=5)

        columns = ("activity_id", "activity", "cost", "enrollments", "income")
        self.activity_tree = ttk.Treeview(self.left_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.activity_tree.heading(col, text=col.capitalize())
        self.activity_tree.column("activity_id", width=80)
        self.activity_tree.column("activity", width=150)
        self.activity_tree.column("cost", width=60)
        self.activity_tree.column("enrollments", width=90)
        self.activity_tree.column("income", width=90)
        self.activity_tree.pack(fill=tk.BOTH, expand=True, pady=5)

        self.activity_tree.bind("<Double-1>", self.on_activity_double_click)

        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(pady=5, fill=tk.X)

        ttk.Button(btn_frame, text="Refresh", command=self.refresh_activities).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add/Update Activity", command=self.show_activity_editor).pack(side=tk.LEFT, padx=5)

        self.current_right = None
        self.refresh_activities()

    def refresh_activities(self):
        for row in self.activity_tree.get_children():
            self.activity_tree.delete(row)
        for act_id, data in activities.items():
            cost = data.get("cost", 0)
            enroll_count = self.count_enrollments(act_id)
            income = cost * enroll_count
            self.activity_tree.insert("", tk.END, values=(act_id, data["activity"], cost, enroll_count, income))
        save_data(activities, students)

    def count_enrollments(self, activity_id):
        count = 0
        for s_data in students.values():
            if activity_id in s_data.get("activities_enrolled", []):
                count += 1
        return count

    def clear_right(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.current_right = None

    def show_activity_editor(self):
        self.clear_right()
        self.current_right = ttk.Frame(self.right_frame, padding=10)
        self.current_right.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.current_right, text="Activity Editor", font=("Arial", 14, "bold")).pack(pady=5)

        ttk.Label(self.current_right, text="Activity ID (leave blank to add new):").pack(anchor=tk.W, pady=5)
        id_entry = ttk.Entry(self.current_right)
        id_entry.pack(fill=tk.X)

        ttk.Label(self.current_right, text="Activity Name:").pack(anchor=tk.W, pady=5)
        name_entry = ttk.Entry(self.current_right)
        name_entry.pack(fill=tk.X)

        ttk.Label(self.current_right, text="Cost:").pack(anchor=tk.W, pady=5)
        cost_entry = ttk.Entry(self.current_right)
        cost_entry.pack(fill=tk.X)

        ttk.Label(self.current_right, text="Start Date (dd/mm/yyyy):").pack(anchor=tk.W, pady=5)
        start_entry = ttk.Entry(self.current_right)
        start_entry.pack(fill=tk.X)

        ttk.Label(self.current_right, text="End Date (dd/mm/yyyy):").pack(anchor=tk.W, pady=5)
        end_entry = ttk.Entry(self.current_right)
        end_entry.pack(fill=tk.X)

        def save_activity():
            act_id_str = id_entry.get().strip()
            act_name = name_entry.get().strip()
            cost_str = cost_entry.get().strip()
            start_date = start_entry.get().strip()
            end_date = end_entry.get().strip()

            if not act_name:
                messagebox.showerror("Error", "Activity Name is required.")
                return
            if not cost_str.isdigit():
                messagebox.showerror("Error", "Cost must be a number.")
                return

            cost_val = int(cost_str)

            if act_id_str:
                try:
                    act_id = int(act_id_str)
                    activities[act_id] = activities.get(act_id, {})
                    activities[act_id].update({
                        "activity": act_name,
                        "cost": cost_val,
                        "start_date": start_date,
                        "end_date": end_date
                    })
                except ValueError:
                    messagebox.showerror("Error", "Activity ID must be an integer.")
                    return
            else:
                new_id = max(activities.keys()) + 1 if activities else 2001
                activities[new_id] = {
                    "activity": act_name,
                    "cost": cost_val,
                    "start_date": start_date,
                    "end_date": end_date,
                    "year_level": "",
                    "location": "",
                    "days": "",
                    "time": "",
                    "teacher_id": None
                }

            self.refresh_activities()
            messagebox.showinfo("Success", "Activity saved successfully.")
            self.clear_right()
            save_data(activities, students)

        ttk.Button(self.current_right, text="Save", command=save_activity).pack(pady=10)

    def on_activity_double_click(self, event):
        selection = self.activity_tree.selection()
        if not selection:
            return
        item = self.activity_tree.item(selection[0], "values")
        if not item:
            return
        act_id = int(item[0])
        self.show_enrolled_students(act_id)

    def show_enrolled_students(self, activity_id):
        self.clear_right()
        self.current_right = ttk.Frame(self.right_frame, padding=10)
        self.current_right.pack(fill=tk.BOTH, expand=True)

        title = f"Students Enrolled in Activity {activity_id}"
        ttk.Label(self.current_right, text=title, font=("Arial", 14, "bold")).pack(anchor=tk.N, pady=5)

        columns = ("student_id", "name", "year_level", "house")
        tree = ttk.Treeview(self.current_right, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col.capitalize())
        tree.pack(fill=tk.BOTH, expand=True)

        for s_id, s_data in students.items():
            if activity_id in s_data.get("activities_enrolled", []):
                name = f"{s_data['firstname']} {s_data['surname']}"
                tree.insert("", tk.END, values=(s_id, name, s_data["year_level"], s_data["house"]))

        def on_student_double(event):
            sel = tree.selection()
            if sel:
                item_vals = tree.item(sel[0], "values")
                st_id = int(item_vals[0])
                info = format_student_info(st_id)
                info_label.config(text=info)

        tree.bind("<Double-1>", on_student_double)

        info_label = ttk.Label(self.current_right, text="", justify=tk.LEFT)
        info_label.pack(fill=tk.X, pady=5)

# -------------------------------------------------------------------
# Staff Frame
# -------------------------------------------------------------------
class StaffFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        ttk.Label(self, text="Staff Panel", font=("Arial", 16, "bold")).pack(anchor=tk.N, pady=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Activities tab
        self.activities_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.activities_tab, text="Activities")

        columns_act = ("activity_id", "activity", "enrollments")
        self.act_tree = ttk.Treeview(self.activities_tab, columns=columns_act, show="headings", height=10)
        for col in columns_act:
            self.act_tree.heading(col, text=col.capitalize())
        self.act_tree.column("activity_id", width=80)
        self.act_tree.column("activity", width=200)
        self.act_tree.column("enrollments", width=100)
        self.act_tree.pack(fill=tk.BOTH, expand=True)

        ttk.Button(self.activities_tab, text="Refresh", command=self.refresh_activities).pack(pady=5)

        # Students tab
        self.students_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.students_tab, text="Students")

        columns_st = ("student_id", "name", "num_activities")
        self.st_tree = ttk.Treeview(self.students_tab, columns=columns_st, show="headings", height=10)
        for col in columns_st:
            self.st_tree.heading(col, text=col.capitalize())
        self.st_tree.column("student_id", width=80)
        self.st_tree.column("name", width=150)
        self.st_tree.column("num_activities", width=120)
        self.st_tree.pack(fill=tk.BOTH, expand=True)

        self.st_tree.bind("<Double-1>", self.on_student_double_click)

        ttk.Button(self.students_tab, text="Refresh", command=self.refresh_students).pack(pady=5)

        self.info_label = ttk.Label(self.students_tab, text="", justify=tk.LEFT)
        self.info_label.pack(fill=tk.X, pady=5)

        self.refresh_activities()
        self.refresh_students()

    def refresh_activities(self):
        for row in self.act_tree.get_children():
            self.act_tree.delete(row)
        for act_id, data in activities.items():
            enroll_count = sum(1 for s in students.values() if act_id in s.get("activities_enrolled", []))
            self.act_tree.insert("", tk.END, values=(act_id, data["activity"], enroll_count))
        save_data(activities, students)

    def refresh_students(self):
        for row in self.st_tree.get_children():
            self.st_tree.delete(row)
        for s_id, s_data in students.items():
            fullname = f"{s_data['firstname']} {s_data['surname']}"
            num = len(s_data.get("activities_enrolled", []))
            self.st_tree.insert("", tk.END, values=(s_id, fullname, num))
        save_data(activities, students)

    def on_student_double_click(self, event):
        selection = self.st_tree.selection()
        if selection:
            item_vals = self.st_tree.item(selection[0], "values")
            student_id = int(item_vals[0])
            info = format_student_info(student_id)
            self.info_label.config(text=info)

# -------------------------------------------------------------------
# Student Frame
# -------------------------------------------------------------------
class StudentFrame(ttk.Frame):
    def __init__(self, parent, student_id):
        super().__init__(parent, padding=10)
        self.student_id = student_id

        title = ttk.Label(self, text="Student Panel", font=("Arial", 16, "bold"))
        title.pack(anchor=tk.N, pady=5)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Notebook with "My Clubs" and "Available Clubs"
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.my_clubs_tab = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(self.my_clubs_tab, text="My Clubs")

        columns = ("club_id", "club_name")
        self.my_clubs_tree = ttk.Treeview(self.my_clubs_tab, columns=columns, show="headings", height=10)
        self.my_clubs_tree.heading("club_id", text="Club ID")
        self.my_clubs_tree.heading("club_name", text="Club Name")
        self.my_clubs_tree.column("club_id", width=80)
        self.my_clubs_tree.column("club_name", width=200)
        self.my_clubs_tree.pack(fill=tk.BOTH, expand=True)
        self.my_clubs_tree.bind("<<TreeviewSelect>>", self.on_my_club_select)

        self.available_clubs_tab = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(self.available_clubs_tab, text="Available Clubs")

        self.available_clubs_tree = ttk.Treeview(self.available_clubs_tab, columns=columns, show="headings", height=10)
        self.available_clubs_tree.heading("club_id", text="Club ID")
        self.available_clubs_tree.heading("club_name", text="Club Name")
        self.available_clubs_tree.column("club_id", width=80)
        self.available_clubs_tree.column("club_name", width=200)
        self.available_clubs_tree.pack(fill=tk.BOTH, expand=True)
        self.available_clubs_tree.bind("<<TreeviewSelect>>", self.on_available_club_select)

        # Right: Club details & action button
        right_frame = ttk.Frame(main_frame, padding=10, relief=tk.GROOVE)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.details_label = ttk.Label(right_frame, text="Club Details", font=("Arial", 14, "bold"))
        self.details_label.pack(anchor=tk.N)

        self.club_details_text = tk.Text(right_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.club_details_text.pack(fill=tk.BOTH, expand=True, pady=5)

        self.action_button = ttk.Button(right_frame, text="", command=self.on_action_button)
        self.action_button.pack(pady=5)

        self.refresh_tabs()

    def refresh_tabs(self):
        # Clear the trees
        for tree in (self.my_clubs_tree, self.available_clubs_tree):
            for item in tree.get_children():
                tree.delete(item)

        student_data = students.get(self.student_id, {})
        enrolled = student_data.get("activities_enrolled", [])

        # Populate My Clubs
        for club_id in enrolled:
            if club_id in activities:
                club_name = activities[club_id]["activity"]
                self.my_clubs_tree.insert("", tk.END, values=(club_id, club_name))

        # Populate Available Clubs
        for club_id, club_data in activities.items():
            if club_id not in enrolled:
                self.available_clubs_tree.insert("", tk.END, values=(club_id, club_data["activity"]))

    def on_my_club_select(self, event):
        selection = self.my_clubs_tree.selection()
        if selection:
            item_vals = self.my_clubs_tree.item(selection[0], "values")
            club_id = int(item_vals[0])
            self.show_club_details(club_id, enrolled=True)

    def on_available_club_select(self, event):
        selection = self.available_clubs_tree.selection()
        if selection:
            item_vals = self.available_clubs_tree.item(selection[0], "values")
            club_id = int(item_vals[0])
            self.show_club_details(club_id, enrolled=False)

    def show_club_details(self, club_id, enrolled):
        club = activities.get(club_id)
        if not club:
            return
        details = (
            f"Club ID: {club_id}\n"
            f"Name: {club['activity']}\n"
            f"Year Level: {club.get('year_level', 'N/A')}\n"
            f"Location: {club.get('location', 'N/A')}\n"
            f"Days: {club.get('days', 'N/A')}\n"
            f"Time: {club.get('time', 'N/A')}\n"
            f"Cost: ${club.get('cost', 'N/A')}\n"
            f"Start Date: {club.get('start_date', 'N/A')}\n"
            f"End Date: {club.get('end_date', 'N/A')}\n"
        )
        teacher_id = club.get("teacher_id")
        if teacher_id and teacher_id in teachers:
            t_data = teachers[teacher_id]
            details += f"Teacher: {t_data['title']} {t_data['firstname']} {t_data['surname']}\n"

        self.club_details_text.config(state=tk.NORMAL)
        self.club_details_text.delete("1.0", tk.END)
        self.club_details_text.insert(tk.END, details)
        self.club_details_text.config(state=tk.DISABLED)

        if enrolled:
            self.action_button.config(text="Leave Club", command=lambda: self.leave_club(club_id))
        else:
            self.action_button.config(text="Join Club", command=lambda: self.join_club(club_id))

    def join_club(self, club_id):
        student_data = students.get(self.student_id, {})
        if club_id not in student_data.get("activities_enrolled", []):
            student_data.setdefault("activities_enrolled", []).append(club_id)
            messagebox.showinfo("Success", f"You have joined {activities[club_id]['activity']}.")
        else:
            messagebox.showinfo("Info", "You are already enrolled in this club.")
        save_data(activities, students)
        self.refresh_tabs()
        self.clear_details()

    def leave_club(self, club_id):
        student_data = students.get(self.student_id, {})
        if club_id in student_data.get("activities_enrolled", []):
            student_data["activities_enrolled"].remove(club_id)
            messagebox.showinfo("Success", f"You have left {activities[club_id]['activity']}.")
        else:
            messagebox.showinfo("Info", "You are not enrolled in this club.")
        save_data(activities, students)
        self.refresh_tabs()
        self.clear_details()

    def clear_details(self):
        self.club_details_text.config(state=tk.NORMAL)
        self.club_details_text.delete("1.0", tk.END)
        self.club_details_text.config(state=tk.DISABLED)
        self.action_button.config(text="")

    def on_action_button(self):
        # This is a placeholder; the actual action is assigned dynamically
        pass

# -------------------------------------------------------------------
# Main entry point
# -------------------------------------------------------------------
def main():
    login_window = LoginWindow()
    login_window.mainloop()

if __name__ == "__main__":
    main()
