# Import tkinter library for GUI elements
import tkinter as tk
# Import themed widgets (ttk) and message boxes from tkinter
from tkinter import ttk, messagebox

# Import shared data dictionaries (activities, students, USERS, teachers)
# and the save_data function from the common.py file.
# 'save_data' is needed here because students can join/leave clubs, modifying the 'students' data.
from common import activities, students, USERS, teachers, save_data

# Define the StudentFrame class, inheriting from ttk.Frame.
# This class represents the main panel for the student view.
class StudentFrame(ttk.Frame):
    """Student panel for viewing and managing their club enrollments."""
    # Constructor method, called when a StudentFrame object is created.
    # 'parent' is the container widget. 'student_id' is the ID of the logged-in student.
    def __init__(self, parent, student_id):
        # Call the parent class (ttk.Frame) constructor, adding padding.
        super().__init__(parent, padding=10)
        # Store the student's ID for later use within this class instance.
        self.student_id = student_id
        # Access the global 'students' dictionary (from common.py) to get this student's data.
        # Use .get() with a default empty dictionary {} in case the ID is somehow invalid.
        student_data = students.get(self.student_id, {})
        # Get the student's first name for the dashboard title, defaulting to "Student".
        student_name = f"{student_data.get('firstname', 'Student')}"

        # Create and place the title label for the student dashboard.
        title = ttk.Label(self, text=f"{student_name}'s Dashboard", font=("Arial", 16, "bold"))
        title.pack(anchor=tk.NW, pady=(0, 10)) # Align top-left, add padding below

        # Create a main frame to hold the left and right panels.
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True) # Make it fill the StudentFrame

        # --- Left Panel: Notebook for Club Lists ---
        # Create the left frame.
        left_frame = ttk.Frame(main_frame)
        # Place it on the left, allow it to fill space, add padding to its right.
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Create a Notebook widget (for tabs) inside the left frame.
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True) # Make the notebook fill the left frame

        # --- "My Clubs" Tab ---
        # Create a frame for the "My Clubs" tab content.
        self.my_clubs_tab = ttk.Frame(self.notebook, padding=5)
        # Add this frame to the notebook as a tab.
        self.notebook.add(self.my_clubs_tab, text="My Clubs")
        # Define columns for the Treeview in this tab.
        columns = ("club_id", "club_name")
        # Create the Treeview widget to list clubs the student is enrolled in.
        self.my_clubs_tree = ttk.Treeview(self.my_clubs_tab, columns=columns, show="headings", height=15)
        # Configure the columns using the helper method.
        self.setup_treeview_columns(self.my_clubs_tree, columns, {"club_id": 80})
        # Place the Treeview within the tab frame.
        self.my_clubs_tree.pack(fill=tk.BOTH, expand=True)
        # Bind the selection event (single click) to the 'on_my_club_select' method.
        self.my_clubs_tree.bind("<<TreeviewSelect>>", self.on_my_club_select)

        # --- "Available Clubs" Tab ---
        # Create a frame for the "Available Clubs" tab content.
        self.available_clubs_tab = ttk.Frame(self.notebook, padding=5)
        # Add this frame to the notebook as a tab.
        self.notebook.add(self.available_clubs_tab, text="Available Clubs")
        # Create the Treeview widget to list clubs the student can join.
        # Uses the same column definition as "My Clubs".
        self.available_clubs_tree = ttk.Treeview(self.available_clubs_tab, columns=columns, show="headings", height=15)
        # Configure the columns.
        self.setup_treeview_columns(self.available_clubs_tree, columns, {"club_id": 80})
        # Place the Treeview within the tab frame.
        self.available_clubs_tree.pack(fill=tk.BOTH, expand=True)
        # Bind the selection event (single click) to the 'on_available_club_select' method.
        self.available_clubs_tree.bind("<<TreeviewSelect>>", self.on_available_club_select)

        # --- Right Panel: Club Details and Action Button ---
        # Create the right frame. Add padding and a visual border.
        right_frame = ttk.Frame(main_frame, padding=10, relief=tk.GROOVE, borderwidth=1)
        # Place it on the right, allow it to fill space, add padding to its left.
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Add a label for the details section.
        self.details_label = ttk.Label(right_frame, text="Club Details", font=("Arial", 14, "bold"))
        self.details_label.pack(anchor=tk.NW, pady=(0, 5)) # Align top-left, add padding below

        # Use a standard tkinter Text widget to display multi-line club details.
        # 'wrap=tk.WORD' makes text wrap at word boundaries.
        # 'state=tk.DISABLED' makes the text read-only initially.
        # 'relief=tk.FLAT' removes the default sunken border of the Text widget.
        self.club_details_text = tk.Text(
            right_frame, height=12, wrap=tk.WORD, state=tk.DISABLED, relief=tk.FLAT
        )
        # --- Style the Text Widget ---
        # Try to match the Text widget's background/foreground to the current ttk theme.
        style = ttk.Style()
        # Look up the background color of a standard ttk Frame.
        text_bg = style.lookup('TFrame', 'background')
        try:
            # Look up the foreground (text) color of a standard ttk Label.
            text_fg = style.lookup('TLabel', 'foreground')
        except tk.TclError:
            # If the lookup fails (e.g., theme doesn't define it), use black as a fallback.
            text_fg = "black"

        # Apply the retrieved or fallback colors to the Text widget.
        # Also remove any highlight border that might appear on focus.
        self.club_details_text.config(
            background=text_bg,
            foreground=text_fg,
            highlightthickness=0, # Remove focus highlight border
            borderwidth=0       # Remove widget border
        )
        # Place the Text widget, allowing it to fill the available space in the right panel.
        self.club_details_text.pack(fill=tk.BOTH, expand=True, pady=5)


        # --- Action Button ---
        # Create the button for joining or leaving a club.
        # Initially disabled and showing "Select a club".
        self.action_button = ttk.Button(right_frame, text="Select a club", state=tk.DISABLED, command=self.perform_club_action)
        # Place the button at the bottom of the right panel.
        self.action_button.pack(pady=10)
        # Initialize variables to keep track of the selected club and the action (join/leave).
        self.selected_club_id = None # Will store the ID (integer) of the club selected in either tree.
        self.current_action = None   # Will store 'join' or 'leave'.

        # --- Initial Data Load ---
        # Call the method to populate the "My Clubs" and "Available Clubs" lists initially.
        self.refresh_tabs() 

    # --- Helper Method ---
    # Method to configure Treeview columns (reused for both club trees).
    def setup_treeview_columns(self, tree, cols, widths=None):
        """Helper to configure Treeview columns."""
        widths = widths or {}
        for col in cols:
            tree.heading(col, text=col.replace("_", " ").title()) # Format heading text
            tree.column(col, width=widths.get(col, 150), anchor=tk.W) # Set width (default 150), align left

    # --- UI Update Methods ---
    # Method to reload data in both the "My Clubs" and "Available Clubs" tabs.
    def refresh_tabs(self):
        """Reload the 'My Clubs' and 'Available Clubs' lists."""
        # Clear existing items from both Treeviews.
        self.my_clubs_tree.delete(*self.my_clubs_tree.get_children())
        self.available_clubs_tree.delete(*self.available_clubs_tree.get_children())

        # Access global 'students' and 'activities' dictionaries from common.py.
        # Get the current student's data.
        student_data = students.get(self.student_id, {})
        # Get the set of IDs of clubs the student is currently enrolled in. Using a set is efficient for checking membership ('in').
        enrolled_ids = set(student_data.get("activities_enrolled", []))
        # Get the student's year level for eligibility checks.
        student_year = student_data.get("year_level")

        # Get all activities and sort them by ID for consistent display order.
        sorted_activities = sorted(activities.items())

        # Iterate through all available activities in the school.
        for club_id, club_data in sorted_activities:
            club_name = club_data.get("activity", "Unknown Club")
            # Get the year level requirement string for the club (e.g., "9-10", "7-12", "11", "N/A").
            allowed_years_str = club_data.get("year_level", "N/A")

            # --- Eligibility Check ---
            is_eligible = False # Assume not eligible initially
            # Only perform check if student year level is known and club has a requirement.
            if student_year is not None and allowed_years_str != "N/A":
                try:
                    # Handle different formats of year level strings:
                    if "all" in allowed_years_str.lower() or allowed_years_str == "7-12":
                        is_eligible = True # Eligible for all years
                    elif "-" in allowed_years_str: # Range format (e.g., "9-10")
                        min_year, max_year = map(int, allowed_years_str.split('-'))
                        if min_year <= student_year <= max_year:
                            is_eligible = True
                    elif "," in allowed_years_str: # List format (e.g., "7, 9, 11")
                         allowed_years = [int(y.strip()) for y in allowed_years_str.split(',')]
                         if student_year in allowed_years:
                             is_eligible = True
                    else: # Single year format (e.g., "10")
                         if int(allowed_years_str) == student_year:
                            is_eligible = True
                except ValueError:
                    # If the year level string is malformed (e.g., "Year 9"), print a warning.
                    # Decide how to handle this: currently defaults to eligible.
                    print(f"Warning: Could not parse year level '{allowed_years_str}' for club {club_id}")
                    is_eligible = True # Default to eligible if parse fails? Or False? Let's stick to True for now.
            elif allowed_years_str == "N/A": # If no year level is specified for the club
                 is_eligible = True # Assume eligible

            # --- Populate Trees ---
            # Check if the student is already enrolled in this club.
            if club_id in enrolled_ids:
                # If enrolled, add it to the "My Clubs" tree.
                self.my_clubs_tree.insert("", tk.END, values=(club_id, club_name))
            # If not enrolled BUT eligible based on year level check.
            elif is_eligible:
                # Add it to the "Available Clubs" tree.
                self.available_clubs_tree.insert("", tk.END, values=(club_id, club_name))

        # After refreshing lists, clear the details panel and reset the action button.
        self.clear_details()

    # Method to display the details of a selected club in the right panel's Text widget.
    def display_club_details(self, club_id):
        """Show details of the selected club in the text area."""
        # Access global 'activities' and 'teachers' dictionaries from common.py.
        # Get the data for the selected club ID.
        club = activities.get(club_id)
        # If the club ID doesn't exist (e.g., data inconsistency), show an error message.
        if not club:
            details = "Club details not found."
        else:
            # If club data exists, format the details into a list of strings.
            details_list = [
                f"Name: {club.get('activity', 'N/A')}",
                f"Year Level(s): {club.get('year_level', 'N/A')}",
                f"Location: {club.get('location', 'N/A')}",
                f"Schedule: {club.get('days', 'N/A')} at {club.get('time', 'N/A')}",
                f"Cost: ${club.get('cost', 0)}",
                f"Dates: {club.get('start_date', 'N/A')} to {club.get('end_date', 'N/A')}"
            ]
            # Get the teacher ID associated with the club.
            teacher_id = club.get("teacher_id")
            teacher_info_str = "Teacher: N/A" # Default string
            # If there is a teacher ID and that ID exists in the 'teachers' dictionary.
            if teacher_id and teacher_id in teachers:
                # Get the teacher's data.
                t_data = teachers[teacher_id]
                # Format the teacher's name (including title).
                teacher_info_str = f"Teacher: {t_data.get('title','')} {t_data.get('firstname','')} {t_data.get('surname','')}"
            # Add the teacher information string to the details list.
            details_list.append(teacher_info_str)

            # Join the list of detail strings into a single multi-line string.
            details = "\n".join(details_list)

        # Update the Text widget with the details.
        self.club_details_text.config(state=tk.NORMAL)    # Temporarily enable writing to the widget.
        self.club_details_text.delete("1.0", tk.END)      # Clear any previous content (from line 1, char 0 to the end).
        self.club_details_text.insert(tk.END, details)    # Insert the new details string.
        self.club_details_text.config(state=tk.DISABLED)  # Disable writing again to make it read-only.

    # Method to update the text and state of the action button (Join/Leave).
    def update_action_button(self, club_id, action_type):
        """Configure the action button (Join/Leave/Contact)."""
        # Store the selected club ID and the type of action ('join' or 'leave').
        self.selected_club_id = club_id
        self.current_action = action_type
        # Set default button text and state.
        button_text = "Select a club"
        button_state = tk.DISABLED

        # Update text and state based on the action type.
        if action_type == 'leave':
            button_text = "Leave Club"
            button_state = tk.NORMAL # Enable the button
        elif action_type == 'join':
            button_text = "Join Club"
            button_state = tk.NORMAL # Enable the button
        # Placeholder for a potential 'contact' action in the future.
        # elif action_type == 'contact':
        #     button_text = "Contact Teacher"
        #     button_state = tk.NORMAL

        # Apply the determined text and state to the actual button widget.
        self.action_button.config(text=button_text, state=button_state)

    # --- Event Handlers ---
    # Method called when a club is selected in the "My Clubs" Treeview.
    def on_my_club_select(self, event):
        """Handle selection in the 'My Clubs' list."""
        # Get the ID(s) of the selected item(s).
        selection = self.my_clubs_tree.selection()
        # Proceed only if an item is selected.
        if selection:
            # --- Deselect item in the other tree ---
            # If an item is currently selected in the "Available Clubs" tree, deselect it
            # to avoid confusion about which club the details panel refers to.
            if self.available_clubs_tree.selection():
                self.available_clubs_tree.selection_remove(self.available_clubs_tree.selection())

            # Get the values (club_id, club_name) from the selected row in "My Clubs".
            item_vals = self.my_clubs_tree.item(selection[0], "values")
            try:
                # Extract the club ID (first value) and convert it to an integer.
                club_id = int(item_vals[0])
                # Display the details for this club ID.
                self.display_club_details(club_id)
                # Update the action button to show "Leave Club" and enable it.
                self.update_action_button(club_id, 'leave')
            except (ValueError, IndexError):
                # If conversion fails or values are missing, clear the details panel.
                self.clear_details()

    # Method called when a club is selected in the "Available Clubs" Treeview.
    def on_available_club_select(self, event):
        """Handle selection in the 'Available Clubs' list."""
        # Get the ID(s) of the selected item(s).
        selection = self.available_clubs_tree.selection()
        # Proceed only if an item is selected.
        if selection:
            # --- Deselect item in the other tree ---
            # If an item is currently selected in the "My Clubs" tree, deselect it.
            if self.my_clubs_tree.selection():
                self.my_clubs_tree.selection_remove(self.my_clubs_tree.selection())

            # Get the values from the selected row in "Available Clubs".
            item_vals = self.available_clubs_tree.item(selection[0], "values")
            try:
                # Extract the club ID and convert to integer.
                club_id = int(item_vals[0])
                # Display the details for this club ID.
                self.display_club_details(club_id)
                # Update the action button to show "Join Club" and enable it.
                self.update_action_button(club_id, 'join')
            except (ValueError, IndexError):
                # If errors occur, clear the details panel.
                self.clear_details()

    # Method called when the action button (Join/Leave) is clicked.
    def perform_club_action(self):
        """Execute the join or leave action based on current state."""
        # Check if a club is selected and an action is defined.
        if not self.selected_club_id or not self.current_action:
            messagebox.showwarning("Action Error", "No club selected or action defined.")
            return # Stop if no valid action can be performed

        # Get the stored club ID and action type.
        club_id = self.selected_club_id
        action = self.current_action
        # Access global 'activities' and 'students' dictionaries.
        # Get the name of the club for use in messages.
        club_name = activities.get(club_id, {}).get("activity", "this club")

        # Get the current student's data.
        student_data = students.get(self.student_id)
        # If student data is somehow missing, show an error and stop.
        if not student_data:
             messagebox.showerror("Error", "Student data not found.")
             return

        # --- Data Integrity Check ---
        # Ensure the 'activities_enrolled' key exists in the student's data
        # and that its value is actually a list before trying to modify it.
        if "activities_enrolled" not in student_data or not isinstance(student_data["activities_enrolled"], list):
            # If missing or not a list, initialize/reset it as an empty list.
            student_data["activities_enrolled"] = []
        # Get a reference to the student's enrollment list.
        enrolled_list = student_data["activities_enrolled"]

        # --- Perform Action ---
        if action == 'join':
            # Check if the student is NOT already enrolled.
            if club_id not in enrolled_list:
                # Add the club ID to the student's enrollment list.
                enrolled_list.append(club_id)
                # Show a success message.
                messagebox.showinfo("Success", f"You have joined '{club_name}'.")
                # --- Save Changes ---
                # Call 'save_data' (from common.py) to write the updated 'students' dictionary
                # (along with other potentially unchanged data) back to the JSON file.
                save_data(activities, students, USERS, teachers)
                # Refresh the UI (both club lists) to reflect the change.
                self.refresh_tabs()
            else:
                # If already enrolled, just inform the user.
                messagebox.showinfo("Info", f"You are already enrolled in '{club_name}'.")
        elif action == 'leave':
            # Check if the student IS currently enrolled.
            if club_id in enrolled_list:
                # Ask for confirmation before leaving the club.
                if messagebox.askyesno("Confirm Leave", f"Are you sure you want to leave '{club_name}'?"):
                    # If confirmed, remove the club ID from the list.
                    enrolled_list.remove(club_id)
                    # Show a success message.
                    messagebox.showinfo("Success", f"You have left '{club_name}'.")
                    # --- Save Changes ---
                    save_data(activities, students, USERS, teachers)
                    # Refresh the UI.
                    self.refresh_tabs()
            else:
                # If not enrolled, inform the user (shouldn't happen if UI is correct, but good check).
                 messagebox.showinfo("Info", f"You are not currently enrolled in '{club_name}'.")
        else:
            # Handle unexpected action types (shouldn't occur with current logic).
            messagebox.showerror("Error", "Unknown action requested.")

    # Method to clear the club details panel and reset the action button.
    def clear_details(self):
        """Clear the details text and disable the action button."""
        # Clear the Text widget and display the default prompt.
        self.club_details_text.config(state=tk.NORMAL) # Enable writing
        self.club_details_text.delete("1.0", tk.END)   # Clear content
        self.club_details_text.insert(tk.END, "Select a club from the lists to see details.") # Insert prompt
        self.club_details_text.config(state=tk.DISABLED) # Disable writing

        # Reset the action button to its default state.
        self.action_button.config(text="Select a club", state=tk.DISABLED)
        # Clear the stored selected club ID and action.
        self.selected_club_id = None
        self.current_action = None
        # --- Deselect items in both trees ---
        # Ensure no items remain visually selected in either Treeview.
        if self.my_clubs_tree.selection():
            self.my_clubs_tree.selection_remove(self.my_clubs_tree.selection())
        if self.available_clubs_tree.selection():
            self.available_clubs_tree.selection_remove(self.available_clubs_tree.selection())