import tkinter as tk
from tkinter import ttk, messagebox

# Import shared data and functions from common.py
from common import activities, students, USERS, teachers, save_data, format_student_info

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
        self.setup_treeview_columns(self.activity_tree, columns, {"cost": 60, "enrollments": 90, "income": 90, "activity_id": 80})
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
        # Access global 'activities' from common.py
        sorted_activities = sorted(activities.items()) # Display sorted by ID

        for act_id, data in sorted_activities:
            cost = data.get("cost", 0)
            enroll_count = self.count_enrollments(act_id)
            income = cost * enroll_count
            self.activity_tree.insert("", tk.END, values=(act_id, data.get("activity", "N/A"), f"${cost}", enroll_count, f"${income}"))

    def count_enrollments(self, activity_id):
        """Count how many students are enrolled in a specific activity."""
        # Access global 'students' from common.py
        return sum(1 for s_data in students.values() if activity_id in s_data.get("activities_enrolled", []))

    def show_activity_editor(self, activity_id_to_edit=None):
        """Display form in the right panel to add or edit an activity."""
        self.clear_right_panel() # Clear previous content

        editor_frame = ttk.Frame(self.right_panel, padding=15)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        # Access global 'activities' from common.py
        activity_data = activities.get(activity_id_to_edit, {}) if activity_id_to_edit else {}
        title = "Edit Activity" if activity_id_to_edit else "Add New Activity"
        ttk.Label(editor_frame, text=title, font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=tk.W)

        # Define fields to edit/add
        fields = {
            "Activity ID": {"entry": ttk.Entry(editor_frame), "value": activity_id_to_edit if activity_id_to_edit else "(Auto-generated)", "row": 1, "state": tk.DISABLED },
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
                 # Access global 'teachers' from common.py
                if teacher_id_val is not None and teacher_id_val not in teachers:
                     messagebox.showwarning("Warning", f"Teacher ID {teacher_id_val} does not exist in the teacher list.")
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

            # Access global 'activities' from common.py
            if activity_id_to_edit: # Editing existing
                act_id = activity_id_to_edit
                activities[act_id].update(updated_data)
                message = "Activity updated successfully."
            else: # Adding new
                new_id = max(list(activities.keys()) + [2000]) + 1 # Ensure it's at least 2001
                activities[new_id] = updated_data
                message = f"Activity '{act_name}' added successfully with ID {new_id}."

            # Call save_data from common.py, passing the global data structures
            save_data(activities, students, USERS, teachers)
            self.refresh_activities() # Update the tree view
            messagebox.showinfo("Success", message)
            self.clear_right_panel("Select an activity or Add/Edit.") # Clear form

        save_button = ttk.Button(editor_frame, text="Save Activity", command=save_activity)
        save_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

    def on_activity_select(self, event):
        """When an activity is selected, show enrolled students in the right panel."""
        selection = self.activity_tree.selection()
        if not selection:
            return
        item_values = self.activity_tree.item(selection[0], "values")
        if not item_values: return

        try:
            act_id = int(item_values[0])
            # Access global 'activities' from common.py
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
        self.setup_treeview_columns(students_tree, columns, {"student_id": 80, "year_level": 80, "house": 100})
        students_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        students_tree.bind("<<TreeviewSelect>>", self.on_student_select) # Bind selection

        # Populate the tree
        enrolled_count = 0
        # Access global 'students' from common.py
        sorted_students_view = sorted(students.items()) # Sort students for consistent display
        for s_id, s_data in sorted_students_view:
            if activity_id in s_data.get("activities_enrolled", []):
                name = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
                students_tree.insert("", tk.END, values=(s_id, name, s_data.get("year_level", 'N/A'), s_data.get("house", 'N/A')))
                enrolled_count += 1

        if enrolled_count == 0:
            ttk.Label(details_frame, text="No students currently enrolled.").pack(pady=10)

        # Add an Edit button for the selected activity below the student list
        edit_button = ttk.Button(details_frame, text=f"Edit '{activity_name}' Details", command=lambda: self.show_activity_editor(activity_id))
        edit_button.pack(pady=(15, 5), anchor=tk.SW) # Add padding

        # Label to display selected student's info
        self.student_info_label_admin = ttk.Label(details_frame, text="Select a student to view details.", justify=tk.LEFT, wraplength=350)
        self.student_info_label_admin.pack(fill=tk.X, pady=10, side=tk.BOTTOM)

    def on_student_select(self, event):
        """Display details of the student selected in the enrolled list."""
        tree = event.widget
        selection = tree.selection()
        if not selection:
            self.student_info_label_admin.config(text="Select a student to view details.")
            return
        vals = tree.item(selection[0], "values")
        try:
            st_id = int(vals[0])
            # Use format_student_info from common.py
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
             # Access global 'activities' from common.py
            act_id = int(item_values[0])
            act_name = activities.get(act_id, {}).get("activity", "this activity")
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Could not identify the selected activity.")
            return

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete '{act_name}' (ID: {act_id})?\nThis will also remove it from all enrolled students."):
            # Remove the activity itself (access global 'activities')
            if act_id in activities:
                del activities[act_id]

            # Remove the activity ID from all students enrolled in it (access global 'students')
            for s_id in list(students.keys()): # Iterate over a copy of keys for safe modification
                if act_id in students[s_id].get("activities_enrolled", []):
                    students[s_id]["activities_enrolled"].remove(act_id)

            # Call save_data from common.py, passing the global data structures
            save_data(activities, students, USERS, teachers)
            self.refresh_activities() # Update the tree
            self.clear_right_panel("Activity deleted. Select another activity or Add/Edit.") # Clear the right panel
            messagebox.showinfo("Deleted", f"Activity '{act_name}' has been deleted.")