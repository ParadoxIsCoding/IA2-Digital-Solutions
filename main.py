import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------------------------------------------------
# Hard-coded user credentials (username -> {password, role, student_id?})
# -------------------------------------------------------------------
USERS = {
    # Administrator account
    "admin": {
        "password": "admin123",
        "role": "administrator"
    },
    # School staff account
    "staff": {
        "password": "staff123",
        "role": "staff"
    },
    # Student accounts (each student user links to a student_id in the students dict)
    "maddi": {
        "password": "student123",
        "role": "student",
        "student_id": 101908
    },
    "laura": {
        "password": "student123",
        "role": "student",
        "student_id": 101920
    },
    "don": {
        "password": "student123",
        "role": "student",
        "student_id": 136111
    },
    "jim": {
        "password": "student123",
        "role": "student",
        "student_id": 136179
    }
}

# -------------------------------------------------------------------
# Sample data for teachers, activities, students
# -------------------------------------------------------------------
teachers = {
    3001: {"firstname": "John", "surname": "Smith", "title": "Mr", "contact": "123-456-7890"},
    3002: {"firstname": "Sarah", "surname": "Connor", "title": "Ms", "contact": "987-654-3210"}
}

# Activities data
activities = {
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
    }
}

# Students data: each student can have multiple enrolled activities in a list
students = {
    101908: {
        "firstname": "Maddi",
        "surname": "Gascar",
        "gender": "Female",
        "year_level": 9,
        "house": "Bradman",
        "dob": "27/06/2005",
        "activities_enrolled": [2001]  # Initially enrolled in Basketball
    },
    101920: {
        "firstname": "Laura",
        "surname": "Norder",
        "gender": "Female",
        "year_level": 11,
        "house": "Chisholm",
        "dob": "31/07/2002",
        "activities_enrolled": [2002]  # Initially enrolled in Chess
    },
    136111: {
        "firstname": "Don",
        "surname": "Keigh",
        "gender": "Male",
        "year_level": 12,
        "house": "Lawson",
        "dob": "14/06/2003",
        "activities_enrolled": [2002]  # Initially enrolled in Chess
    },
    136179: {
        "firstname": "Jim",
        "surname": "Pansey",
        "gender": "Male",
        "year_level": 12,
        "house": "Sturt",
        "dob": "06/10/2002",
        "activities_enrolled": []      # Not enrolled yet
    },
    136180: {
        "firstname": "Harrison",
        "surname": "Chapman",
        "gender": "Non-Binary",
        "year_level": 12,
        "house": "Lawson",
        "dob": "14/06/2003",
        "activities_enrolled": [2002, 2001]  # Enrolled in Chess & Basketball
    },
}

# -------------------------------------------------------------------
# Login Window
# -------------------------------------------------------------------
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x150")
        
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        login_button = ttk.Button(self, text="Login", command=self.check_credentials)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_info = USERS.get(username)
        if user_info and user_info["password"] == password:
            # Successful login
            self.destroy()  # close login window
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
        self.student_id = student_id  # only set if role == 'student'
        
        # Create frames for each role
        self.admin_frame = AdminFrame(self)
        self.staff_frame = StaffFrame(self)
        self.student_frame = StudentFrame(self, self.student_id)
        
        self.show_relevant_frame()

        self.mainloop()

    def show_relevant_frame(self):
        """Hide all frames, then show only the frame for the current role."""
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
            # If unknown role, just show an error or close
            messagebox.showerror("Error", f"Unknown role: {self.role}")
            self.destroy()


# -------------------------------------------------------------------
# Admin Frame (Administrator role)
# -------------------------------------------------------------------
class AdminFrame(ttk.Frame):
    """
    Administrator can:
      - Add/Update extracurricular activity details (no pop-up)
      - Show total income for each activity
      - Double-click an activity to see enrolled students in the side panel
      - Double-click a student (in side panel) to see detailed info below
    """
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        
        # We'll split this frame into two columns: left for activities, right for details
        self.left_frame = ttk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(self, relief=tk.RIDGE)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Title
        ttk.Label(self.left_frame, text="Administrator Panel", font=("Arial", 16, "bold")).pack(anchor=tk.N, pady=5)
        
        # Treeview to show activities
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
        
        # Bind double-click on an activity
        self.activity_tree.bind("<Double-1>", self.on_activity_double_click)

        # Buttons
        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(pady=5, fill=tk.X)

        ttk.Button(btn_frame, text="Refresh", command=self.refresh_activities).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add/Update Activity", command=self.show_activity_editor).pack(side=tk.LEFT, padx=5)
        
        # Right frame: We'll dynamically display either:
        #  - The Add/Update form
        #  - The list of enrolled students
        #  - The student's info
        # We'll keep sub-widgets in memory or create/destroy as needed.

        # Sub-frame for showing enrolled students
        self.enrolled_students_frame = None
        self.students_tree = None
        self.student_info_label = None

        # Sub-frame for the activity editor
        self.activity_editor_frame = None

        # Initially load activities
        self.refresh_activities()

    def refresh_activities(self):
        """Refresh the activity list in the Treeview with enrollments and total income."""
        for row in self.activity_tree.get_children():
            self.activity_tree.delete(row)

        for activity_id, data in activities.items():
            cost = data.get("cost", 0)
            enroll_count = self.count_enrollments(activity_id)
            income = cost * enroll_count
            self.activity_tree.insert(
                "",
                tk.END,
                values=(activity_id, data["activity"], cost, enroll_count, income)
            )

    def count_enrollments(self, activity_id):
        """Count how many students are enrolled in the given activity_id."""
        count = 0
        for s_id, s_data in students.items():
            if activity_id in s_data["activities_enrolled"]:
                count += 1
        return count

    def clear_right_frame(self):
        """Remove any widgets in the right frame before showing something else."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def show_activity_editor(self):
        """Display the Add/Update Activity form in the right frame."""
        self.clear_right_frame()

        self.activity_editor_frame = ttk.Frame(self.right_frame, padding=10)
        self.activity_editor_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.activity_editor_frame, text="Activity Editor", font=("Arial", 14, "bold")).pack(pady=5)

        # Fields
        ttk.Label(self.activity_editor_frame, text="Activity ID (leave blank to add new):").pack(pady=5, anchor=tk.W)
        id_entry = ttk.Entry(self.activity_editor_frame)
        id_entry.pack(fill=tk.X)

        ttk.Label(self.activity_editor_frame, text="Activity Name:").pack(pady=5, anchor=tk.W)
        name_entry = ttk.Entry(self.activity_editor_frame)
        name_entry.pack(fill=tk.X)

        ttk.Label(self.activity_editor_frame, text="Cost:").pack(pady=5, anchor=tk.W)
        cost_entry = ttk.Entry(self.activity_editor_frame)
        cost_entry.pack(fill=tk.X)

        ttk.Label(self.activity_editor_frame, text="Start Date (dd/mm/yyyy):").pack(pady=5, anchor=tk.W)
        start_entry = ttk.Entry(self.activity_editor_frame)
        start_entry.pack(fill=tk.X)

        ttk.Label(self.activity_editor_frame, text="End Date (dd/mm/yyyy):").pack(pady=5, anchor=tk.W)
        end_entry = ttk.Entry(self.activity_editor_frame)
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
                # Update existing or add new
                try:
                    act_id = int(act_id_str)
                    if act_id in activities:
                        # Update existing
                        activities[act_id]["activity"] = act_name
                        activities[act_id]["cost"] = cost_val
                        activities[act_id]["start_date"] = start_date
                        activities[act_id]["end_date"] = end_date
                    else:
                        # Add new
                        activities[act_id] = {
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
                except ValueError:
                    messagebox.showerror("Error", "Activity ID must be an integer.")
                    return
            else:
                # Auto-generate new ID
                new_id = max(activities.keys()) + 1
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
            self.clear_right_frame()  # Clear the form

        ttk.Button(self.activity_editor_frame, text="Save", command=save_activity).pack(pady=10)

    def on_activity_double_click(self, event):
        """When an admin double-clicks an activity, show the enrolled students in the right frame."""
        selection = self.activity_tree.selection()
        if not selection:
            return
        item = selection[0]
        row_values = self.activity_tree.item(item, "values")
        if not row_values:
            return

        activity_id = int(row_values[0])
        self.show_enrolled_students(activity_id)

    def show_enrolled_students(self, activity_id):
        """Show a list of students enrolled in the selected activity in the right frame."""
        self.clear_right_frame()

        self.enrolled_students_frame = ttk.Frame(self.right_frame, padding=10)
        self.enrolled_students_frame.pack(fill=tk.BOTH, expand=True)

        title = f"Students Enrolled in Activity {activity_id}"
        ttk.Label(self.enrolled_students_frame, text=title, font=("Arial", 14, "bold")).pack(anchor=tk.N, pady=5)

        columns = ("student_id", "name", "year_level", "house")
        self.students_tree = ttk.Treeview(self.enrolled_students_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.students_tree.heading(col, text=col.capitalize())
        self.students_tree.pack(fill=tk.BOTH, expand=True)

        # Populate
        for s_id, s_data in students.items():
            if activity_id in s_data["activities_enrolled"]:
                name = f"{s_data['firstname']} {s_data['surname']}"
                year = s_data["year_level"]
                house = s_data["house"]
                self.students_tree.insert("", tk.END, values=(s_id, name, year, house))

        self.students_tree.bind("<Double-1>", self.on_student_double_click)

        # Label to show detailed student info
        self.student_info_label = ttk.Label(self.enrolled_students_frame, text="", justify=tk.LEFT)
        self.student_info_label.pack(fill=tk.X, pady=5)

    def on_student_double_click(self, event):
        """When admin double-clicks a student in the 'enrolled students' tree, show student info below."""
        selection = self.students_tree.selection()
        if not selection:
            return
        item = selection[0]
        vals = self.students_tree.item(item, "values")
        student_id = int(vals[0])
        self.show_student_info(student_id)

    def show_student_info(self, student_id):
        """Update the student_info_label with detailed info."""
        s_data = students.get(student_id)
        if not s_data:
            self.student_info_label.config(text="Student not found.")
            return

        enrolled_activities = s_data.get("activities_enrolled", [])
        if enrolled_activities:
            activity_names = [activities[a_id]["activity"] for a_id in enrolled_activities]
            activities_str = ", ".join(activity_names)
        else:
            activities_str = "None"

        info_str = (
            f"Name: {s_data['firstname']} {s_data['surname']}\n"
            f"Gender: {s_data['gender']}\n"
            f"Year Level: {s_data['year_level']}\n"
            f"House: {s_data['house']}\n"
            f"DOB: {s_data['dob']}\n"
            f"Activities Enrolled: {activities_str}\n"
        )
        self.student_info_label.config(text=info_str)


# -------------------------------------------------------------------
# Staff Frame (Teacher in charge)
# -------------------------------------------------------------------
class StaffFrame(ttk.Frame):
    """
    School Staff can:
      - View a list of activities with total enrollments
      - View a list of all students and how many activities each is enrolled in
      - Double-click on a student to view that student's info below
    """
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        
        ttk.Label(self, text="Staff Panel", font=("Arial", 16, "bold")).pack(anchor=tk.N, pady=5)

        # Notebook to separate "Activities" and "Students"
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Frame for Activities
        self.activities_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.activities_frame, text="Activities")

        # Frame for Students
        self.students_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.students_frame, text="Students")

        # Activities Tree
        columns_activities = ("activity_id", "activity", "enrollments")
        self.activity_tree = ttk.Treeview(self.activities_frame, columns=columns_activities, show="headings", height=10)
        for col in columns_activities:
            self.activity_tree.heading(col, text=col.capitalize())
        self.activity_tree.column("activity_id", width=80)
        self.activity_tree.column("activity", width=200)
        self.activity_tree.column("enrollments", width=100)
        self.activity_tree.pack(fill=tk.BOTH, expand=True)

        ttk.Button(self.activities_frame, text="Refresh", command=self.refresh_activities).pack(pady=5)

        # Students Tree
        columns_students = ("student_id", "name", "num_activities")
        self.student_tree = ttk.Treeview(self.students_frame, columns=columns_students, show="headings", height=10)
        for col in columns_students:
            self.student_tree.heading(col, text=col.capitalize())
        self.student_tree.column("student_id", width=80)
        self.student_tree.column("name", width=150)
        self.student_tree.column("num_activities", width=120)
        self.student_tree.pack(fill=tk.BOTH, expand=True)

        self.student_tree.bind("<Double-1>", self.on_student_double_click)

        ttk.Button(self.students_frame, text="Refresh", command=self.refresh_students).pack(pady=5)

        # Label to show the selected student's info (no new windows)
        self.student_info_label = ttk.Label(self.students_frame, text="", justify=tk.LEFT)
        self.student_info_label.pack(fill=tk.X, pady=5)

        # Initial loads
        self.refresh_activities()
        self.refresh_students()

    def refresh_activities(self):
        for row in self.activity_tree.get_children():
            self.activity_tree.delete(row)
        for activity_id, data in activities.items():
            enroll_count = self.count_enrollments(activity_id)
            self.activity_tree.insert("", tk.END, values=(activity_id, data["activity"], enroll_count))

    def refresh_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for s_id, s_data in students.items():
            fullname = f"{s_data['firstname']} {s_data['surname']}"
            num_activities = len(s_data["activities_enrolled"])
            self.student_tree.insert("", tk.END, values=(s_id, fullname, num_activities))

    def count_enrollments(self, activity_id):
        count = 0
        for s_id, s_data in students.items():
            if activity_id in s_data["activities_enrolled"]:
                count += 1
        return count

    def on_student_double_click(self, event):
        """Show the student's info below the tree (no new window)."""
        selection = self.student_tree.selection()
        if selection:
            item = selection[0]
            vals = self.student_tree.item(item, "values")
            student_id = int(vals[0])
            self.display_student_info(student_id)

    def display_student_info(self, student_id):
        s_data = students.get(student_id)
        if not s_data:
            self.student_info_label.config(text="Student not found.")
            return

        enrolled_activities = s_data.get("activities_enrolled", [])
        if enrolled_activities:
            activity_names = [activities[a_id]["activity"] for a_id in enrolled_activities]
            activities_str = ", ".join(activity_names)
        else:
            activities_str = "None"

        info_str = (
            f"Name: {s_data['firstname']} {s_data['surname']}\n"
            f"Gender: {s_data['gender']}\n"
            f"Year Level: {s_data['year_level']}\n"
            f"House: {s_data['house']}\n"
            f"DOB: {s_data['dob']}\n"
            f"Activities Enrolled: {activities_str}\n"
        )
        self.student_info_label.config(text=info_str)


# -------------------------------------------------------------------
# Student Frame
# -------------------------------------------------------------------
class StudentFrame(ttk.Frame):
    """
    Student can:
      - View available activities
      - Enroll in an activity
    """
    def __init__(self, parent, student_id):
        super().__init__(parent, padding=10)
        self.student_id = student_id
        
        # Title
        ttk.Label(self, text="Student Panel", font=("Arial", 16, "bold")).pack(anchor=tk.N, pady=5)
        
        # Frame for the student's current enrollments
        self.enrolled_label = ttk.Label(self, text="Currently Enrolled Activities:")
        self.enrolled_label.pack(anchor=tk.W, pady=5)

        self.enrolled_listbox = tk.Listbox(self, height=5)
        self.enrolled_listbox.pack(fill=tk.X, pady=5)

        # Frame for all available activities
        self.available_label = ttk.Label(self, text="All Available Activities:")
        self.available_label.pack(anchor=tk.W, pady=5)

        self.activities_listbox = tk.Listbox(self, height=5)
        self.activities_listbox.pack(fill=tk.X, pady=5)

        # Button to enroll
        ttk.Button(self, text="Enroll in Selected Activity", command=self.enroll_in_activity).pack(pady=5)

        # Refresh to show data
        self.refresh_lists()

    def refresh_lists(self):
        """Refresh the enrolled and available activity lists."""
        self.enrolled_listbox.delete(0, tk.END)
        self.activities_listbox.delete(0, tk.END)

        student_data = students.get(self.student_id, {})
        enrolled_ids = student_data.get("activities_enrolled", [])

        # Fill the "currently enrolled" list
        for a_id in enrolled_ids:
            act_name = activities[a_id]["activity"]
            self.enrolled_listbox.insert(tk.END, f"{a_id} - {act_name}")

        # Fill the "all available" list (activities not enrolled)
        for a_id, a_data in activities.items():
            if a_id not in enrolled_ids:
                self.activities_listbox.insert(tk.END, f"{a_id} - {a_data['activity']}")

    def enroll_in_activity(self):
        """Enroll the student in the selected activity from the 'available' list."""
        selection = self.activities_listbox.curselection()
        if not selection:
            return

        selected_line = self.activities_listbox.get(selection[0])
        # The line is something like "2001 - Basketball"
        a_id_str = selected_line.split()[0]
        try:
            a_id = int(a_id_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid activity selection.")
            return

        student_data = students.get(self.student_id)
        if student_data is None:
            messagebox.showerror("Error", "Student data not found.")
            return

        if a_id not in student_data["activities_enrolled"]:
            student_data["activities_enrolled"].append(a_id)
            messagebox.showinfo("Success", f"You have enrolled in {activities[a_id]['activity']}.")
        else:
            messagebox.showinfo("Info", "You are already enrolled in this activity.")

        self.refresh_lists()


# -------------------------------------------------------------------
# Main entry point
# -------------------------------------------------------------------
def main():
    login_window = LoginWindow()
    login_window.mainloop()

if __name__ == "__main__":
    main()
