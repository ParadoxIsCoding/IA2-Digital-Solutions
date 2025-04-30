# Import the tkinter library for creating graphical user interfaces (GUIs)
import tkinter as tk
# Import specific widgets (ttk for themed widgets, messagebox for pop-up messages)
from tkinter import ttk, messagebox

# Import shared data (dictionaries like activities, students, USERS, teachers)
# and functions (save_data, format_student_info) from the common.py file.
# This allows different parts of the application to access the same information.
from common import activities, students, USERS, teachers, save_data, format_student_info

# Define a class named AdminFrame, which inherits from ttk.Frame.
# This class represents the main panel for the administrator view.
class AdminFrame(ttk.Frame):
    """Admin panel for managing activities and viewing enrollments."""
    # The __init__ method is the constructor, called when an AdminFrame object is created.
    # 'parent' is the container widget (like the main window) where this frame will be placed.
    def __init__(self, parent):
        # Call the constructor of the parent class (ttk.Frame) to initialize the frame.
        # 'padding=10' adds some space around the frame's content.
        super().__init__(parent, padding=10)

        # --- Layout Setup ---
        # Create a frame for the left side of the admin panel.
        left_panel = ttk.Frame(self)
        # Place the left panel on the left side, make it fill available space vertically and horizontally.
        # 'expand=True' allows it to grow if the window is resized. 'padx=(0, 5)' adds padding only on the right.
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Create a frame for the right side of the admin panel.
        # 'relief=tk.GROOVE' gives it a sunken border style. 'borderwidth=1' sets the border thickness.
        self.right_panel = ttk.Frame(self, relief=tk.GROOVE, borderwidth=1) # Add border for visual separation
        # Place the right panel on the right side, make it fill available space. 'padx=(5, 0)' adds padding only on the left.
        self.left_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # --- Left Panel Content (Activities Overview) ---
        # Add a label widget to the left panel for the title.
        # 'font=("Arial", 16, "bold")' sets the font style.
        # 'anchor=tk.NW' aligns the label to the top-left (North-West). 'pady=(0, 10)' adds padding below the label.
        ttk.Label(left_panel, text="Activities Overview", font=("Arial", 16, "bold")).pack(anchor=tk.NW, pady=(0, 10))

        # Create a Treeview widget to display the list of activities in a table format.
        # Define the column identifiers.
        columns = ("activity_id", "activity", "cost", "enrollments", "income")
        # Create the Treeview widget, assign columns, hide the default first column ('#0'), set height.
        self.activity_tree = ttk.Treeview(left_panel, columns=columns, show="headings", height=15)
        # Call a helper method to configure the appearance of the columns (headings, widths).
        # Pass the tree, column names, and specific widths for some columns.
        self.setup_treeview_columns(self.activity_tree, columns, {"cost": 60, "enrollments": 90, "income": 90, "activity_id": 80})
        # Place the Treeview in the left panel, making it fill the available space.
        self.activity_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        # Bind the '<<TreeviewSelect>>' event (when an item is selected) to the 'on_activity_select' method.
        self.activity_tree.bind("<<TreeviewSelect>>", self.on_activity_select)

        # Create a frame to hold the buttons below the activity list.
        btn_frame = ttk.Frame(left_panel)
        # Place the button frame below the tree, make it fill horizontally, align to bottom-left.
        btn_frame.pack(pady=10, fill=tk.X, anchor=tk.SW)
        # Create a "Refresh List" button, linking its click action to the 'refresh_activities' method.
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_activities).pack(side=tk.LEFT, padx=5)
        # Create an "Add/Edit Activity" button, linking its click action to the 'show_activity_editor' method.
        ttk.Button(btn_frame, text="Add/Edit Activity", command=self.show_activity_editor).pack(side=tk.LEFT, padx=5)
        # Create a "Delete Activity" button, linking its click action to the 'delete_selected_activity' method.
        ttk.Button(btn_frame, text="Delete Activity", command=self.delete_selected_activity).pack(side=tk.LEFT, padx=5)

        # --- Right Panel Initial State ---
        # Call a method to clear the right panel and display an initial message.
        self.clear_right_panel("Select an activity to see details or edit.")
        # Call the method to load and display the initial list of activities in the treeview.
        self.refresh_activities() # Load initial data

    # --- Helper Methods ---

    # Method to configure the columns of a Treeview widget.
    def setup_treeview_columns(self, tree, cols, widths=None):
        """Helper to configure Treeview columns."""
        # Initialize widths dictionary if not provided.
        widths = widths or {}
        # Loop through each column identifier.
        for col in cols:
            # Set the heading text for the column (replace underscores with spaces, capitalize words).
            tree.heading(col, text=col.replace("_", " ").title()) # Make headings readable
            # Set the column width (use provided width or default to 100), align content to the left (West).
            tree.column(col, width=widths.get(col, 100), anchor=tk.W) # Default width 100

    # Method to clear all widgets from the right panel.
    def clear_right_panel(self, message=""):
        """Clear the right panel and optionally display a message."""
        # Loop through all widgets currently inside the right panel.
        for widget in self.right_panel.winfo_children():
            # Remove the widget.
            widget.destroy()
        # If a message is provided, display it as a label.
        if message:
            ttk.Label(self.right_panel, text=message, padding=10, wraplength=300).pack(pady=20)

    # Method to reload and display the activity data in the main Treeview.
    def refresh_activities(self):
        """Reload and display activity data in the treeview."""
        # Delete all existing items currently in the activity tree.
        self.activity_tree.delete(*self.activity_tree.get_children()) # Clear existing items
        # Access the global 'activities' dictionary imported from common.py.
        # Sort the activities by their ID (key) before displaying.
        sorted_activities = sorted(activities.items()) # Display sorted by ID

        # Loop through each activity ID and its data in the sorted list.
        for act_id, data in sorted_activities:
            # Get the cost, defaulting to 0 if not found.
            cost = data.get("cost", 0)
            # Count how many students are enrolled in this activity using a helper method.
            enroll_count = self.count_enrollments(act_id)
            # Calculate the total income for this activity.
            income = cost * enroll_count
            # Insert a new row into the activity tree with the calculated values.
            # Format cost and income as currency strings.
            self.activity_tree.insert("", tk.END, values=(act_id, data.get("activity", "N/A"), f"${cost}", enroll_count, f"${income}"))

    # Method to count enrollments for a specific activity ID.
    def count_enrollments(self, activity_id):
        """Count how many students are enrolled in a specific activity."""
        # Access the global 'students' dictionary imported from common.py.
        # Use a generator expression and sum() to count students.
        # It checks if the 'activity_id' is present in the 'activities_enrolled' list for each student.
        return sum(1 for s_data in students.values() if activity_id in s_data.get("activities_enrolled", []))

    # Method to display the form for adding a new activity or editing an existing one.
    def show_activity_editor(self, activity_id_to_edit=None):
        """Display form in the right panel to add or edit an activity."""
        # Clear any existing content from the right panel.
        self.clear_right_panel() # Clear previous content

        # Create a new frame within the right panel to hold the editor form.
        editor_frame = ttk.Frame(self.right_panel, padding=15)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        # Access the global 'activities' dictionary.
        # If 'activity_id_to_edit' is provided, get the data for that activity.
        # Otherwise, use an empty dictionary (for adding a new activity).
        activity_data = activities.get(activity_id_to_edit, {}) if activity_id_to_edit else {}
        # Set the title based on whether we are editing or adding.
        title = "Edit Activity" if activity_id_to_edit else "Add New Activity"
        # Display the title label in the editor frame.
        ttk.Label(editor_frame, text=title, font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=tk.W)

        # Define the input fields for the activity form using a dictionary.
        # Each key is the label text. The value is another dictionary containing:
        # - 'entry': The ttk.Entry widget for input.
        # - 'value': The initial value to display (from activity_data or default).
        # - 'row': The grid row number for placement.
        # - 'state': (Optional) Set to tk.DISABLED for non-editable fields like Activity ID.
        fields = {
            "Activity ID": {"entry": ttk.Entry(editor_frame), "value": activity_id_to_edit if activity_id_to_edit else "(Auto-generated)", "row": 1, "state": tk.DISABLED },
            "Activity Name": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("activity", ""), "row": 2},
            "Year Level": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("year_level", ""), "row": 3},
            "Location": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("location", ""), "row": 4},
            "Days": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("days", ""), "row": 5},
            "Time": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("time", ""), "row": 6},
            "Cost ($)": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("cost", ""), "row": 7},
            "Teacher ID": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("teacher_id", ""), "row": 8},
            "Start Date (DD/MM/YYYY)": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("start_date", ""), "row": 9},
            "End Date (DD/MM/YYYY)": {"entry": ttk.Entry(editor_frame), "value": activity_data.get("end_date", ""), "row": 10}
        }

        # Loop through the defined fields to create labels and entry widgets.
        for label_text, config in fields.items():
            # Create the label for the field.
            label = ttk.Label(editor_frame, text=label_text + ":")
            # Place the label in the grid. 'sticky=tk.W' aligns it to the left (West).
            label.grid(row=config["row"], column=0, padx=5, pady=5, sticky=tk.W)
            # Get the entry widget associated with this field.
            entry = config["entry"]
            # Insert the initial value into the entry widget.
            entry.insert(0, config["value"])
            # Place the entry widget in the grid. 'sticky=tk.EW' makes it stretch horizontally (East-West).
            entry.grid(row=config["row"], column=1, padx=5, pady=5, sticky=tk.EW)
            # If a 'state' is defined (like tk.DISABLED), apply it to the entry widget.
            if "state" in config:
                entry.config(state=config["state"])

        # Make the second column (containing entry widgets) expand horizontally if the window is resized.
        editor_frame.columnconfigure(1, weight=1)

        # Create a frame to hold the Save and Cancel buttons.
        button_frame = ttk.Frame(editor_frame)
        # Place the button frame below the input fields, spanning both columns.
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=15)

        # Create the Save button.
        # The 'command' uses a lambda function to pass the necessary arguments (fields dictionary and activity ID)
        # to the 'save_activity' method when the button is clicked.
        save_button = ttk.Button(button_frame, text="Save Activity", command=lambda: self.save_activity(fields, activity_id_to_edit))
        # Place the Save button on the left side of the button frame.
        save_button.pack(side=tk.LEFT, padx=10)

        # Create the Cancel button.
        # Its command calls 'clear_right_panel' to remove the editor and show the initial message.
        cancel_button = ttk.Button(button_frame, text="Cancel", command=lambda: self.clear_right_panel("Select an activity to see details or edit."))
        # Place the Cancel button next to the Save button.
        cancel_button.pack(side=tk.LEFT, padx=10)

    # Method called when an item in the main activity Treeview is selected.
    def on_activity_select(self, event):
        """Handle selection in the main activity list. Show enrolled students or edit form."""
        # Get the ID of the selected item in the activity tree.
        selection = self.activity_tree.selection()
        # If nothing is selected (e.g., user clicked empty space), do nothing.
        if not selection:
            # Clear the right panel and show the default message.
            self.clear_right_panel("Select an activity to see details or edit.")
            return

        # Get the first selected item (Treeview allows multiple selections, but we only handle the first).
        selected_item = selection[0]
        # Retrieve the values (data) stored in the selected row.
        item_values = self.activity_tree.item(selected_item, "values")

        # Check if the retrieved values are valid.
        if not item_values:
            self.clear_right_panel("Error: Could not retrieve activity data.")
            return

        try:
            # Extract the activity ID (first value) and convert it to an integer.
            activity_id = int(item_values[0])
            # Extract the activity name (second value).
            activity_name = item_values[1]
            # Call the method to display the list of students enrolled in this activity.
            self.show_enrolled_students(activity_id, activity_name)
        except (ValueError, IndexError) as e:
            # Handle potential errors if the ID is not a valid integer or if values are missing.
            print(f"Error processing activity selection: {e}") # Log error for debugging
            self.clear_right_panel(f"Error displaying details for activity ID {item_values[0]}.")

    # Method to display the list of students enrolled in a specific activity.
    def show_enrolled_students(self, activity_id, activity_name):
        """Display enrolled students for the selected activity in the right panel."""
        # Clear the right panel before adding new content.
        self.clear_right_panel()

        # Create a frame within the right panel to hold the enrolled students list.
        enroll_frame = ttk.Frame(self.right_panel, padding=10)
        enroll_frame.pack(fill=tk.BOTH, expand=True)

        # Display a title showing which activity's enrollments are being viewed.
        ttk.Label(enroll_frame, text=f"Students Enrolled in: {activity_name} (ID: {activity_id})", font=("Arial", 14, "bold")).pack(anchor=tk.NW, pady=(0, 10))

        # Define the columns for the enrolled students Treeview.
        cols = ("student_id", "name", "year_level", "house")
        # Create the Treeview widget.
        student_tree = ttk.Treeview(enroll_frame, columns=cols, show="headings", height=12)
        # Configure the columns using the helper method.
        self.setup_treeview_columns(student_tree, cols, {"year_level": 80, "house": 100, "student_id": 80})
        # Place the Treeview, making it fill the available space.
        student_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        # Bind the selection event to the 'on_student_select' method (to potentially show more details later, though not implemented here).
        student_tree.bind("<<TreeviewSelect>>", self.on_student_select)

        # Populate the Treeview with enrolled students.
        enrolled_count = 0
        # Access the global 'students' dictionary.
        # Sort students by ID for consistent display order.
        sorted_students_view = sorted(students.items())
        # Iterate through all students.
        for s_id, s_data in sorted_students_view:
            # Check if the current student is enrolled in the selected activity.
            if activity_id in s_data.get("activities_enrolled", []):
                # Construct the student's full name.
                fullname = f"{s_data.get('firstname', '')} {s_data.get('surname', '')}"
                # Insert the student's information into the Treeview.
                student_tree.insert("", tk.END, values=(s_id, fullname, s_data.get("year_level", "N/A"), s_data.get("house", "N/A")))
                enrolled_count += 1

        # If no students are enrolled, display a message below the (empty) tree.
        if enrolled_count == 0:
            ttk.Label(enroll_frame, text="No students currently enrolled in this activity.").pack(pady=10)

        # Add buttons below the student list.
        button_frame = ttk.Frame(enroll_frame)
        button_frame.pack(pady=10, anchor=tk.SW) # Align bottom-left

        # Button to go back to the activity editor for the *currently selected* activity in the main list.
        # This reuses the 'show_activity_editor' method.
        edit_button = ttk.Button(button_frame, text="Edit This Activity", command=lambda act_id=activity_id: self.show_activity_editor(act_id))
        edit_button.pack(side=tk.LEFT, padx=5)

        # Button to close the enrolled students view and return to the default right panel message.
        close_button = ttk.Button(button_frame, text="Close View", command=lambda: self.clear_right_panel("Select an activity to see details or edit."))
        close_button.pack(side=tk.LEFT, padx=5)


    # Method called when a student is selected in the 'enrolled students' Treeview.
    # Currently, this method doesn't do anything significant, but it's here as a placeholder
    # if functionality like showing detailed student info on selection is needed later.
    def on_student_select(self, event):
        """Placeholder for handling selection in the enrolled students list."""
        # Get the selected item(s).
        selection = event.widget.selection() # event.widget refers to the tree that triggered the event
        if selection:
            # Get the values of the selected student row.
            student_values = event.widget.item(selection[0], "values")
            # Print the selected student's ID to the console (for debugging/demonstration).
            print(f"Selected student ID (from enrolled list): {student_values[0]}")
            # Future enhancement: Could display full student details here if needed.
        else:
            # Handle deselection if necessary.
            print("Student deselected.")


    # Method to delete the activity currently selected in the main activity Treeview.
    def delete_selected_activity(self):
        """Delete the selected activity after confirmation."""
        # Get the ID(s) of the selected item(s) in the main activity tree.
        selection = self.activity_tree.selection()
        # If nothing is selected, show an info message and do nothing.
        if not selection:
            messagebox.showinfo("Delete Activity", "Please select an activity from the list to delete.")
            return

        # Get the first selected item.
        selected_item = selection[0]
        # Retrieve the values (data) from the selected row.
        item_values = self.activity_tree.item(selected_item, "values")

        # Check if values were retrieved successfully.
        if not item_values:
            messagebox.showerror("Error", "Could not retrieve activity data for deletion.")
            return

        try:
            # Extract the activity ID and name.
            activity_id = int(item_values[0])
            activity_name = item_values[1]

            # --- Check for Enrollments ---
            # Count how many students are currently enrolled in this activity.
            enrollment_count = self.count_enrollments(activity_id)

            # Prepare the confirmation message.
            confirm_message = f"Are you sure you want to delete the activity:\n'{activity_name}' (ID: {activity_id})?"
            # If there are enrollments, add a warning to the message.
            if enrollment_count > 0:
                confirm_message += f"\n\nWarning: {enrollment_count} student(s) are currently enrolled. Deleting the activity will NOT automatically unenroll them (manual cleanup might be needed in student records if this feature isn't added)."

            # Show a confirmation dialog box ('askyesno' returns True for Yes, False for No).
            if messagebox.askyesno("Confirm Deletion", confirm_message):
                # --- Perform Deletion ---
                # Check if the activity ID exists in the global 'activities' dictionary.
                if activity_id in activities:
                    # Remove the activity from the dictionary.
                    del activities[activity_id]
                    # --- Optional: Unenroll students (Good Practice) ---
                    # Iterate through all students and remove this activity_id from their enrollment list.
                    for s_id, s_data in students.items():
                        if activity_id in s_data.get("activities_enrolled", []):
                            s_data["activities_enrolled"].remove(activity_id)
                            print(f"Unenrolled student {s_id} from deleted activity {activity_id}") # Log action

                    # Save the updated data (activities and students) to the JSON file.
                    save_data(activities, students, USERS, teachers)
                    # Show a success message.
                    messagebox.showinfo("Success", f"Activity '{activity_name}' deleted successfully.")
                    # Refresh the activity list in the GUI to reflect the deletion.
                    self.refresh_activities()
                    # Clear the right panel as the deleted activity's details are no longer relevant.
                    self.clear_right_panel("Activity deleted. Select another activity.")
                else:
                    # If the activity ID wasn't found (shouldn't happen if list is up-to-date).
                    messagebox.showerror("Error", "Activity not found in data. It might have been deleted already.")
                    self.refresh_activities() # Refresh list just in case

        except (ValueError, IndexError) as e:
            # Handle errors during ID conversion or value access.
            messagebox.showerror("Error", f"An error occurred during deletion: {e}")
            print(f"Error deleting activity: {e}") # Log detailed error

    # Method to save a new or edited activity.
    def save_activity(self, fields, activity_id_to_edit=None):
        """Save new or edited activity data."""
        # Create a dictionary to hold the data extracted from the form fields.
        new_data = {}
        # Loop through the 'fields' dictionary (which contains the entry widgets).
        for label, config in fields.items():
            # Get the value entered by the user in the corresponding entry widget.
            # .strip() removes leading/trailing whitespace.
            value = config["entry"].get().strip()
            # Convert the user-friendly label back to the dictionary key used in 'activities'.
            # (e.g., "Activity Name" -> "activity", "Cost ($)" -> "cost")
            # Skip the "Activity ID" field as it's handled separately.
            if label == "Activity Name": key = "activity"
            elif label == "Year Level": key = "year_level"
            elif label == "Location": key = "location"
            elif label == "Days": key = "days"
            elif label == "Time": key = "time"
            elif label == "Cost ($)": key = "cost"
            elif label == "Teacher ID": key = "teacher_id"
            elif label == "Start Date (DD/MM/YYYY)": key = "start_date"
            elif label == "End Date (DD/MM/YYYY)": key = "end_date"
            else: continue # Skip Activity ID field

            # --- Basic Input Validation ---
            # Check if essential fields are empty.
            if not value and key in ["activity", "cost", "teacher_id"]: # Example required fields
                 messagebox.showerror("Input Error", f"'{label}' cannot be empty.")
                 return # Stop saving

            # Validate and convert 'Cost' and 'Teacher ID' to integers.
            if key == "cost":
                try:
                    # Attempt to convert the cost value to an integer.
                    new_data[key] = int(value)
                except ValueError:
                    # If conversion fails, show an error and stop saving.
                    messagebox.showerror("Input Error", "'Cost' must be a valid number (e.g., 25).")
                    return
            elif key == "teacher_id":
                try:
                    # Attempt to convert the teacher ID to an integer.
                    teacher_id_val = int(value)
                    # --- Check if Teacher ID exists ---
                    # Access the global 'teachers' dictionary.
                    if teacher_id_val not in teachers:
                        # If the entered Teacher ID doesn't exist in the loaded teacher data.
                        messagebox.showerror("Input Error", f"Teacher ID '{teacher_id_val}' does not exist.")
                        return # Stop saving
                    # Store the valid integer teacher ID.
                    new_data[key] = teacher_id_val
                except ValueError:
                    # If conversion fails, show an error.
                    messagebox.showerror("Input Error", "'Teacher ID' must be a valid number (e.g., 3001).")
                    return
            else:
                # For other fields, store the value as a string.
                new_data[key] = value

        # --- Determine if Adding or Editing ---
        if activity_id_to_edit is None:
            # --- Adding New Activity ---
            # Find the next available activity ID.
            # If 'activities' is not empty, start from max existing ID + 1.
            # Otherwise, start from a base ID (e.g., 2001).
            if activities:
                new_id = max(activities.keys()) + 1
            else:
                new_id = 2001 # Starting ID if no activities exist
            # Add the new activity data to the global 'activities' dictionary using the new ID.
            activities[new_id] = new_data
            # Set success message for adding.
            success_message = f"Activity '{new_data['activity']}' added successfully with ID {new_id}."
        else:
            # --- Editing Existing Activity ---
            # Check if the activity ID still exists (it should, but double-check).
            if activity_id_to_edit in activities:
                # Update the existing entry in the 'activities' dictionary with the new data.
                activities[activity_id_to_edit].update(new_data)
                # Set success message for editing.
                success_message = f"Activity '{new_data['activity']}' (ID: {activity_id_to_edit}) updated successfully."
            else:
                # If the ID somehow disappeared, show an error.
                messagebox.showerror("Error", "Activity ID not found. Cannot update.")
                return

        # --- Save and Update GUI ---
        # Save all data (including the changes to 'activities') to the JSON file.
        save_data(activities, students, USERS, teachers)
        # Show the appropriate success message.
        messagebox.showinfo("Success", success_message)
        # Refresh the main activity list in the GUI to show the changes.
        self.refresh_activities()
        # Clear the right panel (remove the editor form) and show the default message.
        self.clear_right_panel("Select an activity to see details or edit.")