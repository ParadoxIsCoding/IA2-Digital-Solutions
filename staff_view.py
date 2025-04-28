# Import tkinter library for GUI elements
import tkinter as tk
# Import themed widgets from tkinter
from tkinter import ttk

# Import shared data (activities, students dictionaries) and the
# utility function 'format_student_info' from the common.py file.
from common import activities, students, format_student_info

# Define the StaffFrame class, inheriting from ttk.Frame.
# This class represents the main panel for the staff view.
class StaffFrame(ttk.Frame):
    """Staff panel for viewing activities, enrollments, and student details."""
    # Constructor method, called when a StaffFrame object is created.
    # 'parent' is the container widget (like the main application window's content frame).
    def __init__(self, parent):
        # Call the parent class (ttk.Frame) constructor, adding padding.
        super().__init__(parent, padding=10)
        # Add a title label for the staff dashboard.
        ttk.Label(self, text="Staff Dashboard", font=("Arial", 16, "bold")).pack(anchor=tk.NW, pady=(0, 10))

        # Create a Notebook widget (for tabs) within the StaffFrame.
        self.notebook = ttk.Notebook(self)
        # Place the notebook, making it fill the available space.
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # --- Activities Tab ---
        # Create a frame to hold the content of the first tab.
        self.activities_tab = ttk.Frame(self.notebook, padding=10)
        # Add this frame to the notebook as a tab with the specified text label.
        self.notebook.add(self.activities_tab, text="View Activities & Enrollments")

        # Split the "Activities" tab into two vertical sections (left and right).
        # Left frame for listing activities and enrolled students.
        act_list_frame = ttk.Frame(self.activities_tab)
        act_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5)) # Place on left, add right padding
        # Right frame for displaying details of a selected student. Add a border for visual separation.
        self.student_details_frame = ttk.Frame(self.activities_tab, relief=tk.GROOVE, borderwidth=1)
        self.student_details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0)) # Place on right, add left padding

        # --- Widgets within the Left Frame of Activities Tab ---
        # Label for the activities list.
        ttk.Label(act_list_frame, text="Select Activity:", font=("Arial", 12)).pack(anchor=tk.NW)
        # Define columns for the activities Treeview.
        columns_act = ("activity_id", "activity", "enrollments")
        # Create the Treeview widget for activities.
        self.act_tree = ttk.Treeview(act_list_frame, columns=columns_act, show="headings", height=10)
        # Configure the columns (headings, widths) using the helper method.
        self.setup_treeview_columns(self.act_tree, columns_act, {"enrollments": 100, "activity_id": 80})
        # Place the Treeview, making it fill space.
        self.act_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        # Bind the selection event (single click) to the 'on_activity_select' method.
        self.act_tree.bind("<<TreeviewSelect>>", self.on_activity_select)

        # Label for the enrolled students list (below the activities list).
        ttk.Label(act_list_frame, text="Enrolled Students:", font=("Arial", 12)).pack(anchor=tk.NW, pady=(10,0)) # Add padding above
        # Define columns for the enrolled students Treeview.
        cols_students = ("student_id", "name", "year_level")
        # Create the Treeview widget for enrolled students.
        self.act_students_tree = ttk.Treeview(act_list_frame, columns=cols_students, show="headings", height=8)
        # Configure its columns.
        self.setup_treeview_columns(self.act_students_tree, cols_students, {"year_level": 80, "student_id": 80})
        # Place the Treeview.
        self.act_students_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        # Bind the selection event (single click) to the 'on_enrolled_student_select' method.
        self.act_students_tree.bind("<<TreeviewSelect>>", self.on_enrolled_student_select)

        # Add a refresh button at the bottom of the left frame.
        ttk.Button(act_list_frame, text="Refresh Lists", command=self.refresh_activities).pack(pady=10, anchor=tk.SW) # Align bottom-left

        # --- Widgets within the Right Frame of Activities Tab ---
        # Label for the student information area.
        ttk.Label(self.student_details_frame, text="Student Information", font=("Arial", 14, "bold")).pack(pady=10, anchor=tk.NW)
        # Create a label to display the selected student's details.
        # 'justify=tk.LEFT' aligns multi-line text left. 'wraplength' prevents long lines.
        self.student_info_label_act = ttk.Label(self.student_details_frame, text="Select an activity, then select a student from the 'Enrolled Students' list.", justify=tk.LEFT, wraplength=350, padding=10)
        # Place the label, making it fill the available space.
        self.student_info_label_act.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)


        # --- Students Tab ---
        # Create a frame to hold the content of the second tab.
        self.students_tab = ttk.Frame(self.notebook, padding=10)
        # Add this frame to the notebook as the "View All Students" tab.
        self.notebook.add(self.students_tab, text="View All Students")

        # Split the "Students" tab vertically, similar to the "Activities" tab.
        # Left frame for the list of all students.
        student_list_frame = ttk.Frame(self.students_tab)
        student_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        # Right frame for displaying details of a selected student from the main list.
        self.student_info_frame_st = ttk.Frame(self.students_tab, relief=tk.GROOVE, borderwidth=1)
        self.student_info_frame_st.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # --- Widgets within the Left Frame of Students Tab ---
        # Label for the main student list.
        ttk.Label(student_list_frame, text="All Students:", font=("Arial", 12)).pack(anchor=tk.NW)
        # Define columns for the all students Treeview.
        columns_st = ("student_id", "name", "year", "house", "num_activities")
        # Create the Treeview widget. Set a larger height.
        self.st_tree = ttk.Treeview(student_list_frame, columns=columns_st, show="headings", height=20)
        # Configure its columns.
        self.setup_treeview_columns(self.st_tree, columns_st, {"student_id": 80, "year": 60, "house": 80, "num_activities": 100})
        # Place the Treeview.
        self.st_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        # Bind the Double-Click event (<Double-1>) to the 'on_student_double_click' method.
        self.st_tree.bind("<Double-1>", self.on_student_double_click)
        # Bind the single-click selection event to 'on_student_single_click' to provide a hint.
        self.st_tree.bind("<<TreeviewSelect>>", self.on_student_single_click)

        # Add a refresh button for the student list.
        ttk.Button(student_list_frame, text="Refresh Student List", command=self.refresh_students).pack(pady=10, anchor=tk.SW)

        # --- Widgets within the Right Frame of Students Tab ---
        # Label for the student information area.
        ttk.Label(self.student_info_frame_st, text="Student Information", font=("Arial", 14, "bold")).pack(pady=10, anchor=tk.NW)
        # Create a label to display details of the double-clicked student.
        self.info_label_st = ttk.Label(self.student_info_frame_st, text="Double-click a student in the list to view details.", justify=tk.LEFT, wraplength=350, padding=10)
        # Place the label.
        self.info_label_st.pack(fill=tk.BOTH, expand=True, anchor=tk.NW)

        # --- Initial Data Population ---
        # Call the refresh methods to load data into the Treeviews when the StaffFrame is created.
        self.refresh_activities()
        self.refresh_students()

    # --- Helper Method ---
    # Method to configure the columns of a Treeview widget (reused for all trees).
    def setup_treeview_columns(self, tree, cols, widths=None):
        """Helper to configure Treeview columns."""
        widths = widths or {} # Default to empty dict if no widths provided
        for col in cols:
            # Set column heading text (replace underscores, capitalize).
            tree.heading(col, text=col.replace("_", " ").title())
            # Set column width (use provided or default), align content left (West).
            tree.column(col, width=widths.get(col, 120), anchor=tk.W) # Default width 120

    # --- Refresh Methods ---
    # Method to reload data for the Activities tab (activity list).
    def refresh_activities(self):
        """Reload data for the activities tree and clear student list/details."""
        # Clear existing items from the activity tree.
        self.act_tree.delete(*self.act_tree.get_children())
        # Access the global 'activities' and 'students' dictionaries from common.py.
        # Sort activities by ID for consistent order.
        sorted_activities = sorted(activities.items()) # Sort by ID

        # Loop through each activity.
        for act_id, data in sorted_activities:
            # Count enrollments for this activity by checking the 'students' dictionary.
            enroll_count = sum(1 for s in students.values() if act_id in s.get("activities_enrolled", []))
            # Insert the activity data into the activity tree.
            self.act_tree.insert("", tk.END, values=(act_id, data.get("activity", "N/A"), enroll_count))

        # Clear the enrolled students tree associated with the activities tab.
        self.act_students_tree.delete(*self.act_students_tree.get_children())
        # Reset the student details label in the right panel of the activities tab.
        self.student_info_label_act.config(text="Select an activity, then select a student from the 'Enrolled Students' list.")

    # Method to reload data for the Students tab (all students list).
    def refresh_students(self):
        """Reload data for the main student list."""
        # Clear existing items from the main student list tree.
        self.st_tree.delete(*self.st_tree.get_children())
        # Access the global 'students' dictionary from common.py.
        # Sort students by ID.
        sorted_students = sorted(students.items()) # Sort by ID

        # Loop through each student.
        for s_id, s_data in sorted_students:
            # Construct the full name.
            fullname = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
            # Count the number of activities the student is enrolled in.
            num_act = len(s_data.get("activities_enrolled", []))
            # Insert the student data into the main student tree.
            self.st_tree.insert("", tk.END, values=(s_id, fullname, s_data.get("year_level", "N/A"), s_data.get("house", "N/A"), num_act))
        # Reset the student details label in the right panel of the students tab.
        self.info_label_st.config(text="Double-click a student in the list to view details.")

    # --- Event Handlers ---
    # Method called when an activity is selected in the 'act_tree' (Activities Tab).
    def on_activity_select(self, event):
        """Update the 'Enrolled Students' list when an activity is clicked."""
        # Get the selected item ID(s).
        selection = self.act_tree.selection()
        if not selection: return # Do nothing if nothing selected
        # Get the values from the selected row.
        item_vals = self.act_tree.item(selection[0], "values")
        if not item_vals: return # Do nothing if row has no values

        try:
            # Get the activity ID (first value) and convert to integer.
            activity_id = int(item_vals[0])
            # Clear the 'Enrolled Students' tree ('act_students_tree').
            self.act_students_tree.delete(*self.act_students_tree.get_children())
            # Update the details label to prompt selection from the student list.
            self.student_info_label_act.config(text="Select a student from the list above.")

            enrolled_count = 0
            # Access the global 'students' dictionary.
            # Sort students by ID before iterating.
            sorted_students_view = sorted(students.items()) # Sort students
            # Loop through all students to find those enrolled in the selected activity.
            for s_id, s_data in sorted_students_view:
                # Check if the activity_id is in the student's enrollment list.
                if activity_id in s_data.get("activities_enrolled", []):
                    # Construct name and get year level.
                    name = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
                    year = s_data.get("year_level", 'N/A')
                    # Insert the enrolled student into the 'act_students_tree'.
                    self.act_students_tree.insert("", tk.END, values=(s_id, name, year))
                    enrolled_count += 1
            # If no students were found, update the details label.
            if enrolled_count == 0:
                 self.student_info_label_act.config(text="No students enrolled in this activity.")

        except (ValueError, IndexError):
            # Handle errors during ID conversion or value access.
             self.student_info_label_act.config(text="Error loading student list.")

    # Method called when a student is selected in the 'act_students_tree' (Activities Tab).
    def on_enrolled_student_select(self, event):
        """Display details of the student selected from the 'Enrolled Students' list."""
        # Get the selected item ID(s).
        selection = self.act_students_tree.selection()
        if not selection:
            # If deselected, reset the label.
            self.student_info_label_act.config(text="Select a student from the list above.")
            return
        # Get values from the selected row.
        vals = self.act_students_tree.item(selection[0], "values")
        try:
            # Get the student ID (first value) and convert to integer.
            student_id = int(vals[0])
            # Use the 'format_student_info' function (from common.py) to get formatted details.
            info = format_student_info(student_id)
            # Update the details label ('student_info_label_act') in the right frame of the Activities tab.
            self.student_info_label_act.config(text=info)
        except (ValueError, IndexError):
            # Handle errors.
            self.student_info_label_act.config(text="Could not retrieve student details.")

    # Method called on single-click in the main student list ('st_tree' in Students Tab).
    def on_student_single_click(self, event):
        """Provide hint on single click in the all students list."""
        # Check if an item is actually selected.
        if self.st_tree.selection():
             # Update the info label in the right frame of the Students tab to remind user to double-click.
             self.info_label_st.config(text="Double-click the selected student to view details.")

    # Method called on double-click in the main student list ('st_tree' in Students Tab).
    def on_student_double_click(self, event):
        """Display details of the student double-clicked in the main 'Students' tab."""
        # Get the selected item ID(s).
        selection = self.st_tree.selection()
        if not selection: return # Do nothing if nothing selected (e.g., double-click empty space)
        # Get values from the selected row.
        item_vals = self.st_tree.item(selection[0], "values")
        try:
            # Get the student ID (first value) and convert to integer.
            student_id = int(item_vals[0])
            # Use 'format_student_info' (from common.py) to get formatted details.
            info = format_student_info(student_id)
            # Update the details label ('info_label_st') in the right frame of the Students tab.
            self.info_label_st.config(text=info)
        except (ValueError, IndexError):
            # Handle errors.
            self.info_label_st.config(text="Could not retrieve student details.")