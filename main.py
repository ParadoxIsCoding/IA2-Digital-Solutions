# Import necessary libraries from tkinter for the GUI
import tkinter as tk
from tkinter import ttk, messagebox # ttk for themed widgets, messagebox for pop-ups
from sys import exit # Used to stop the application if critical data fails to load

# Import shared data dictionaries (USERS, students, teachers, activities) from common.py.
# These are loaded from data.json by common.py when it's first imported.
from common import USERS, students, teachers, activities # Import all data globals

# Import the custom Frame classes defined in other files for different user views.
from admin_view import AdminFrame   # The view for administrators
from staff_view import StaffFrame   # The view for staff members
from student_view import StudentFrame # The view for students

# --- Initial Data Load Checks ---
# These checks run immediately after imports, ensuring essential data is available before creating the GUI.

# Check if the USERS dictionary (loaded from common.py) is empty.
# User data is critical for login, so the app shouldn't start without it.
if not USERS:
    # Show a fatal error message box.
    messagebox.showerror("Fatal Error", "User data could not be loaded. Application cannot start.")
    # Exit the application immediately.
    exit() # Or handle more gracefully (e.g., show a config screen)

# Check if the teachers dictionary is empty.
# This might be less critical than users, so just show a warning.
if not teachers:
    messagebox.showwarning("Startup Warning", "Teacher data could not be loaded. Teacher details may be missing.")
    # Ensure 'teachers' is at least an empty dictionary if it somehow ended up as None
    # (though common.py's load_data should prevent this).
    if teachers is None: teachers = {}


# --- GUI Classes ---

# Define the Login Window class, inheriting from tk.Tk (the main window class).
class LoginWindow(tk.Tk):
    # Constructor method, called when a LoginWindow object is created.
    def __init__(self):
        # Call the parent class (tk.Tk) constructor.
        super().__init__()
        # Set the title of the login window.
        self.title("Login - Extracurricular Program")
        # Set the initial size of the window (width x height).
        self.geometry("450x260") # Slightly larger for comfort
        # Prevent the user from resizing the login window.
        self.resizable(False, False) # Prevent resizing

        # --- Styling ---
        # Create a ttk Style object to manage widget appearances.
        style = ttk.Style(self)
        # Attempt to set the theme to "clam" for a modern look.
        # Themes might vary depending on the OS and Tk version.
        try:
            style.theme_use("clam") # 'clam', 'alt', 'default', 'classic' are common options
        except tk.TclError:
            # If "clam" theme is not available, print a message and use the default theme.
            print("Clam theme not found, using default.")
            style.theme_use("default")

        # Define some fallback colors in case system theme colors aren't suitable.
        frame_bg = "#f0f0f0" # Light gray background
        label_fg = "black"   # Black text for labels
        entry_bg = "white"   # White background for input fields
        entry_fg = "black"   # Black text for input fields

        # Configure the style for specific ttk widgets.
        style.configure("TFrame", background=frame_bg) # Set background for frames
        style.configure("TLabel", background=frame_bg, foreground=label_fg) # Set background/foreground for labels
        style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg) # Set background/foreground for entry fields
        style.configure("TButton", padding=5) # Add some internal padding to buttons

        # --- Widgets ---
        # Create a main frame within the window to hold all content, add padding.
        main_frame = ttk.Frame(self, padding=20)
        # Place the main frame, making it fill the entire window.
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add a title label inside the main frame.
        ttk.Label(main_frame, text="Please Login", font=("Arial", 20, "bold")).pack(pady=15) # Add vertical padding

        # Create a frame to hold the username label and entry field.
        user_frame = ttk.Frame(main_frame)
        user_frame.pack(pady=5, fill=tk.X) # Add padding, fill horizontally
        # Add the "Username:" label, fix its width, align text left.
        ttk.Label(user_frame, text="Username:", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        # Create the username entry widget.
        self.username_entry = ttk.Entry(user_frame, width=30)
        # Place the entry field, allow it to expand horizontally.
        self.username_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        # Set the initial keyboard focus to the username field.
        self.username_entry.focus()

        # Create a frame for the password label and entry field.
        pass_frame = ttk.Frame(main_frame)
        pass_frame.pack(pady=5, fill=tk.X)
        # Add the "Password:" label.
        ttk.Label(pass_frame, text="Password:", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=5)
        # Create the password entry widget, using 'show="*"' to hide the input.
        self.password_entry = ttk.Entry(pass_frame, show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        # Bind the Enter key press event in the password field to the 'check_credentials' method.
        self.password_entry.bind("<Return>", self.check_credentials)

        # Create the Login button.
        login_button = ttk.Button(main_frame, text="Login", command=self.check_credentials)
        # Also bind the Enter key to the button (optional, provides another way to trigger login).
        login_button.bind("<Return>", self.check_credentials)
        login_button.pack(pady=20) # Add vertical padding

    # Method called when the Login button is clicked or Enter is pressed.
    # 'event=None' is needed because the key binding passes an event object.
    def check_credentials(self, event=None):
        """Validate entered username and password."""
        # Get the text from the username and password entry fields, remove leading/trailing whitespace.
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Access the globally loaded USERS dictionary (from common.py).
        # Try to get the user information associated with the entered username.
        user_info = USERS.get(username)

        # Check if the username exists (user_info is not None) AND
        # if the stored password matches the entered password.
        if user_info and user_info["password"] == password:
            # If credentials are valid:
            self.destroy() # Close the login window.
            # Create and launch the main application window, passing the user's role
            # and student_id (if available, otherwise it will be None).
            MainApplication(role=user_info["role"], student_id=user_info.get("student_id"))
        else:
            # If credentials are invalid:
            # Show an error message box.
            messagebox.showerror("Login Failed", "Invalid username or password.")
            # Clear the password field for security and convenience.
            self.password_entry.delete(0, tk.END)
            # Optionally, move the focus back to the username field.
            self.username_entry.focus() # Keep focus on username

# Define the Main Application Window class, inheriting from tk.Tk.
class MainApplication(tk.Tk):
    # Constructor method. Takes the user's role and optional student_id as arguments.
    def __init__(self, role, student_id=None):
        # Call the parent class (tk.Tk) constructor.
        super().__init__()
        # Store the user's role and student ID.
        self.role = role
        self.student_id = student_id

        # Set the window title, incorporating the user's role.
        self.title(f"Extracurricular Program - {role.capitalize()} View")
        # Set the initial size of the main application window.
        self.geometry("950x600") # Adjusted size

        # Apply the same theme used in the login window for consistency.
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            style.theme_use("default")

        # --- Top Bar Layout ---
        # Create a frame for the top bar (title and logout button).
        top_frame = ttk.Frame(self, padding=(10, 5)) # Add padding (horizontal, vertical)
        top_frame.pack(side=tk.TOP, fill=tk.X) # Place at top, fill horizontally
        # Add the main application title label to the left side of the top bar.
        ttk.Label(top_frame, text="Extracurricular Program Management", font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        # Add a Logout button to the right side of the top bar.
        logout_btn = ttk.Button(top_frame, text="Logout", command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=10) # Add horizontal padding

        # --- Main Content Area ---
        # Create a frame to hold the main content (the role-specific view).
        self.content_frame = ttk.Frame(self, padding=10)
        # Place the content frame, making it fill the remaining space.
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Call the method to load the appropriate view (Admin, Staff, or Student)
        # into the content_frame based on the user's role.
        self.load_role_frame()

        # Start the Tkinter event loop for this window. This makes the window interactive.
        # Note: Typically, mainloop() is called only once on the initial window (LoginWindow in this case).
        # Calling it here means the MainApplication runs its own event loop after login.
        # This is acceptable but slightly less common than managing frames within a single mainloop.
        # self.mainloop() # This might be redundant if LoginWindow().mainloop() is the primary loop. Let's remove it for now.

    # Method to load the correct user interface frame based on the role.
    def load_role_frame(self):
        """Creates and displays the frame based on the user's role."""
        # Clear any widgets currently in the content_frame.
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Check the user's role and instantiate the corresponding Frame class.
        if self.role == "administrator":
            # Create an instance of AdminFrame (from admin_view.py), passing the content_frame as its parent.
            AdminFrame(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif self.role == "staff":
             # Create an instance of StaffFrame (from staff_view.py).
            StaffFrame(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif self.role == "student":
             # Create an instance of StudentFrame (from student_view.py).
             # Student view requires the student_id.
            if self.student_id:
                # Double-check if the student_id actually exists in the loaded student data.
                # Access the global 'students' dictionary from common.py.
                if self.student_id in students:
                    # Create the StudentFrame, passing the content_frame and student_id.
                    StudentFrame(self.content_frame, self.student_id).pack(fill=tk.BOTH, expand=True)
                else:
                    # If the student ID from login doesn't match any student record.
                    messagebox.showerror("Error", f"Student ID {self.student_id} not found in student data.")
                    self.logout() # Log out and return to login screen.
            else:
                # If the role is student but no student_id was provided during login.
                messagebox.showerror("Error", "Student ID not found for student login.")
                self.logout() # Log out.
        else:
            # If the role is unrecognized.
            messagebox.showerror("Error", f"Unknown user role: {self.role}")
            self.logout() # Log out.

    # Method called when the Logout button is clicked.
    def logout(self):
        """Log out the current user and return to the login screen."""
        # Destroy the current MainApplication window.
        self.destroy()
        # Create a new instance of the LoginWindow to show the login screen again.
        # Call mainloop() on the new LoginWindow to start its event loop.
        LoginWindow().mainloop()

# --- Main Execution Block ---
# This is the entry point of the application.

def main():
    """Start the application by creating and showing the login window."""
    # Create an instance of the LoginWindow.
    login_window = LoginWindow()
    # Start the Tkinter event loop for the login window.
    # The application will wait here until the login window is closed.
    login_window.mainloop()

# The standard Python construct to ensure the main() function is called
# only when the script is executed directly (not when imported as a module).
if __name__ == "__main__":
    main()