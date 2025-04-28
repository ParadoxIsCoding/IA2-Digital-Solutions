import tkinter as tk
from tkinter import ttk, messagebox

# Import shared data and functions from common.py
from common import activities, students, USERS, teachers, save_data # Needs save_data for join/leave

class StudentFrame(ttk.Frame):
    """Student panel for viewing and managing their club enrollments."""
    def __init__(self, parent, student_id):
        super().__init__(parent, padding=10)
        self.student_id = student_id
        # Access global 'students' from common.py
        student_data = students.get(self.student_id, {})
        student_name = f"{student_data.get('firstname', 'Student')}" # Get student's first name for title

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
        self.details_label.pack(anchor=tk.NW, pady=(0, 5))

        # Use Text widget for multi-line details, disable editing
        self.club_details_text = tk.Text(
            right_frame, height=12, wrap=tk.WORD, state=tk.DISABLED, relief=tk.FLAT
        )
        # Set background and foreground explicitly for better theme matching
        style = ttk.Style()
        text_bg = style.lookup('TFrame', 'background') # Get default frame background
        try:
            text_fg = style.lookup('TLabel', 'foreground')
        except tk.TclError:
            text_fg = "black" # Fallback color

        self.club_details_text.config(
            background=text_bg,
            foreground=text_fg, # Set foreground color explicitly
            highlightthickness=0, # Remove border highlight
            borderwidth=0 # Remove border
        )
        self.club_details_text.pack(fill=tk.BOTH, expand=True, pady=5)


        # Action button (Join/Leave/Contact)
        self.action_button = ttk.Button(right_frame, text="Select a club", state=tk.DISABLED, command=self.perform_club_action)
        self.action_button.pack(pady=10)
        self.selected_club_id = None # Store the currently selected club ID
        self.current_action = None # Store 'join', 'leave', or 'contact'

        self.refresh_tabs() # Load initial data

    def setup_treeview_columns(self, tree, cols, widths=None):
        """Helper to configure Treeview columns."""
        widths = widths or {}
        for col in cols:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=widths.get(col, 150), anchor=tk.W) # Default width 150

    def refresh_tabs(self):
        """Reload the 'My Clubs' and 'Available Clubs' lists."""
        self.my_clubs_tree.delete(*self.my_clubs_tree.get_children())
        self.available_clubs_tree.delete(*self.available_clubs_tree.get_children())

        # Access global 'students' and 'activities' from common.py
        student_data = students.get(self.student_id, {})
        enrolled_ids = set(student_data.get("activities_enrolled", [])) # Use a set for faster lookups
        student_year = student_data.get("year_level")

        sorted_activities = sorted(activities.items()) # Sort by ID

        # Populate both trees, considering year level restrictions for available clubs
        for club_id, club_data in sorted_activities:
            club_name = club_data.get("activity", "Unknown Club")
            allowed_years_str = club_data.get("year_level", "N/A")

            is_eligible = False
            if student_year is not None and allowed_years_str != "N/A":
                try:
                    if "all" in allowed_years_str.lower() or allowed_years_str == "7-12":
                        is_eligible = True
                    elif "-" in allowed_years_str: # Range like "9-10"
                        min_year, max_year = map(int, allowed_years_str.split('-'))
                        if min_year <= student_year <= max_year:
                            is_eligible = True
                    elif "," in allowed_years_str: # List like "7, 9, 11"
                         allowed_years = [int(y.strip()) for y in allowed_years_str.split(',')]
                         if student_year in allowed_years:
                             is_eligible = True
                    else: # Single year like "10"
                         if int(allowed_years_str) == student_year:
                            is_eligible = True
                except ValueError:
                    print(f"Warning: Could not parse year level '{allowed_years_str}' for club {club_id}")
                    is_eligible = True # Default to eligible if parse fails? Or False? Let's stick to True for now.
            elif allowed_years_str == "N/A": # If no year level is specified, assume eligible
                 is_eligible = True


            if club_id in enrolled_ids:
                self.my_clubs_tree.insert("", tk.END, values=(club_id, club_name))
            elif is_eligible:
                self.available_clubs_tree.insert("", tk.END, values=(club_id, club_name))

        self.clear_details()

    def display_club_details(self, club_id):
        """Show details of the selected club in the text area."""
        # Access global 'activities' and 'teachers' from common.py
        club = activities.get(club_id)
        if not club:
            details = "Club details not found."
        else:
            details_list = [
                f"Name: {club.get('activity', 'N/A')}",
                f"Year Level(s): {club.get('year_level', 'N/A')}",
                f"Location: {club.get('location', 'N/A')}",
                f"Schedule: {club.get('days', 'N/A')} at {club.get('time', 'N/A')}",
                f"Cost: ${club.get('cost', 0)}",
                f"Dates: {club.get('start_date', 'N/A')} to {club.get('end_date', 'N/A')}"
            ]
            teacher_id = club.get("teacher_id")
            teacher_info_str = "Teacher: N/A"
            if teacher_id and teacher_id in teachers:
                t_data = teachers[teacher_id]
                teacher_info_str = f"Teacher: {t_data.get('title','')} {t_data.get('firstname','')} {t_data.get('surname','')}"
            details_list.append(teacher_info_str)

            details = "\n".join(details_list)

        self.club_details_text.config(state=tk.NORMAL) # Enable writing
        self.club_details_text.delete("1.0", tk.END) # Clear previous content
        self.club_details_text.insert(tk.END, details)
        self.club_details_text.config(state=tk.DISABLED) # Disable editing

    def update_action_button(self, club_id, action_type):
        """Configure the action button (Join/Leave/Contact)."""
        self.selected_club_id = club_id
        self.current_action = action_type
        button_text = "Select a club"
        button_state = tk.DISABLED

        if action_type == 'leave':
            button_text = "Leave Club"
            button_state = tk.NORMAL
        elif action_type == 'join':
            button_text = "Join Club"
            button_state = tk.NORMAL
        # Add 'contact' case if needed later
        # elif action_type == 'contact':
        #     button_text = "Contact Teacher"
        #     button_state = tk.NORMAL

        self.action_button.config(text=button_text, state=button_state)

    def on_my_club_select(self, event):
        """Handle selection in the 'My Clubs' list."""
        selection = self.my_clubs_tree.selection()
        if selection:
            # Deselect item in the other tree if one is selected
            if self.available_clubs_tree.selection():
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
            # Deselect item in the other tree if one is selected
            if self.my_clubs_tree.selection():
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
        # Access global 'activities' and 'students' from common.py
        club_name = activities.get(club_id, {}).get("activity", "this club")

        student_data = students.get(self.student_id)
        if not student_data:
             messagebox.showerror("Error", "Student data not found.")
             return

        # Ensure 'activities_enrolled' exists and is a list before modifying
        if "activities_enrolled" not in student_data or not isinstance(student_data["activities_enrolled"], list):
            student_data["activities_enrolled"] = []
        enrolled_list = student_data["activities_enrolled"]

        if action == 'join':
            if club_id not in enrolled_list:
                enrolled_list.append(club_id)
                messagebox.showinfo("Success", f"You have joined '{club_name}'.")
                # Call save_data from common.py, passing the global data structures
                save_data(activities, students, USERS, teachers)
                self.refresh_tabs() # Update UI
            else:
                messagebox.showinfo("Info", f"You are already enrolled in '{club_name}'.")
        elif action == 'leave':
            if club_id in enrolled_list:
                if messagebox.askyesno("Confirm Leave", f"Are you sure you want to leave '{club_name}'?"):
                    enrolled_list.remove(club_id)
                    messagebox.showinfo("Success", f"You have left '{club_name}'.")
                    # Call save_data from common.py, passing the global data structures
                    save_data(activities, students, USERS, teachers)
                    self.refresh_tabs() # Update UI
            else:
                 messagebox.showinfo("Info", f"You are not currently enrolled in '{club_name}'.")
        else:
            messagebox.showerror("Error", "Unknown action requested.")

    def clear_details(self):
        """Clear the details text and disable the action button."""
        self.club_details_text.config(state=tk.NORMAL)
        self.club_details_text.delete("1.0", tk.END)
        self.club_details_text.insert(tk.END, "Select a club from the lists to see details.")
        self.club_details_text.config(state=tk.DISABLED)

        self.action_button.config(text="Select a club", state=tk.DISABLED)
        self.selected_club_id = None
        self.current_action = None
        # Deselect items in both trees
        if self.my_clubs_tree.selection():
            self.my_clubs_tree.selection_remove(self.my_clubs_tree.selection())
        if self.available_clubs_tree.selection():
            self.available_clubs_tree.selection_remove(self.available_clubs_tree.selection())