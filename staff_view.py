import tkinter as tk
from tkinter import ttk

# Import shared data and functions from common.py
from common import activities, students, format_student_info

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
        self.setup_treeview_columns(self.act_tree, columns_act, {"enrollments": 100, "activity_id": 80})
        self.act_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.act_tree.bind("<<TreeviewSelect>>", self.on_activity_select) # Single-click action

        # Treeview for enrolled students (within the same left frame)
        ttk.Label(act_list_frame, text="Enrolled Students:", font=("Arial", 12)).pack(anchor=tk.NW, pady=(10,0))
        cols_students = ("student_id", "name", "year_level")
        self.act_students_tree = ttk.Treeview(act_list_frame, columns=cols_students, show="headings", height=8)
        self.setup_treeview_columns(self.act_students_tree, cols_students, {"year_level": 80, "student_id": 80})
        self.act_students_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.act_students_tree.bind("<<TreeviewSelect>>", self.on_enrolled_student_select) # Single-click action

        # Refresh button for activities tab
        ttk.Button(act_list_frame, text="Refresh Lists", command=self.refresh_activities).pack(pady=10, anchor=tk.SW)

        # Display area for selected student's info (in the right frame)
        ttk.Label(self.student_details_frame, text="Student Information", font=("Arial", 14, "bold")).pack(pady=10, anchor=tk.NW)
        self.student_info_label_act = ttk.Label(self.student_details_frame, text="Select an activity, then select a student from the 'Enrolled Students' list.", justify=tk.LEFT, wraplength=350, padding=10)
        self.student_info_label_act.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)


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
        self.setup_treeview_columns(self.st_tree, columns_st, {"student_id": 80, "year": 60, "house": 80, "num_activities": 100})
        self.st_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.st_tree.bind("<Double-1>", self.on_student_double_click) # Double-click action
        self.st_tree.bind("<<TreeviewSelect>>", self.on_student_single_click) # Single-click for hint

        # Refresh button for students tab
        ttk.Button(student_list_frame, text="Refresh Student List", command=self.refresh_students).pack(pady=10, anchor=tk.SW)

        # Display area for selected student's info (in the right frame)
        ttk.Label(self.student_info_frame_st, text="Student Information", font=("Arial", 14, "bold")).pack(pady=10, anchor=tk.NW)
        self.info_label_st = ttk.Label(self.student_info_frame_st, text="Double-click a student in the list to view details.", justify=tk.LEFT, wraplength=350, padding=10)
        self.info_label_st.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)

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
        self.act_tree.delete(*self.act_tree.get_children())
        # Access global 'activities' and 'students' from common.py
        sorted_activities = sorted(activities.items()) # Sort by ID

        for act_id, data in sorted_activities:
            enroll_count = sum(1 for s in students.values() if act_id in s.get("activities_enrolled", []))
            self.act_tree.insert("", tk.END, values=(act_id, data.get("activity", "N/A"), enroll_count))

        self.act_students_tree.delete(*self.act_students_tree.get_children())
        self.student_info_label_act.config(text="Select an activity, then select a student from the 'Enrolled Students' list.")

    def refresh_students(self):
        """Reload data for the main student list."""
        self.st_tree.delete(*self.st_tree.get_children())
        # Access global 'students' from common.py
        sorted_students = sorted(students.items()) # Sort by ID

        for s_id, s_data in sorted_students:
            fullname = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
            num_act = len(s_data.get("activities_enrolled", []))
            self.st_tree.insert("", tk.END, values=(s_id, fullname, s_data.get("year_level", "N/A"), s_data.get("house", "N/A"), num_act))
        self.info_label_st.config(text="Double-click a student in the list to view details.")

    def on_activity_select(self, event):
        """Update the 'Enrolled Students' list when an activity is clicked."""
        selection = self.act_tree.selection()
        if not selection: return
        item_vals = self.act_tree.item(selection[0], "values")
        if not item_vals: return

        try:
            activity_id = int(item_vals[0])
            self.act_students_tree.delete(*self.act_students_tree.get_children())
            self.student_info_label_act.config(text="Select a student from the list above.")

            enrolled_count = 0
            # Access global 'students' from common.py
            sorted_students_view = sorted(students.items()) # Sort students
            for s_id, s_data in sorted_students_view:
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
        if not selection:
            self.student_info_label_act.config(text="Select a student from the list above.")
            return
        vals = self.act_students_tree.item(selection[0], "values")
        try:
            student_id = int(vals[0])
            # Use format_student_info from common.py
            info = format_student_info(student_id)
            self.student_info_label_act.config(text=info) # Update label in the right frame
        except (ValueError, IndexError):
            self.student_info_label_act.config(text="Could not retrieve student details.")

    def on_student_single_click(self, event):
        """Provide hint on single click in the all students list."""
        if self.st_tree.selection():
             self.info_label_st.config(text="Double-click the selected student to view details.")

    def on_student_double_click(self, event):
        """Display details of the student double-clicked in the main 'Students' tab."""
        selection = self.st_tree.selection()
        if not selection: return
        item_vals = self.st_tree.item(selection[0], "values")
        try:
            student_id = int(item_vals[0])
            # Use format_student_info from common.py
            info = format_student_info(student_id)
            self.info_label_st.config(text=info) # Update label in the right frame of students tab
        except (ValueError, IndexError):
            self.info_label_st.config(text="Could not retrieve student details.")