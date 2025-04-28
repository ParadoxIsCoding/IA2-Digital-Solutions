import tkinter as tk
from tkinter import ttk, messagebox
from sys import exit # For fatal error exit

# Import shared data (needed for checks and passing to views)
from common import USERS, students, teachers, activities # Import all data globals

# Import the view frame classes
from admin_view import AdminFrame
from staff_view import StaffFrame
from student_view import StudentFrame

# --- Check if essential data loaded ---
# Perform these checks after loading data in common.py but before starting GUI
if not USERS:
    messagebox.showerror("Fatal Error", "User data could not be loaded. Application cannot start.")
    exit() # Or handle more gracefully
if not teachers:
     # This might be less critical, maybe just show a warning
    messagebox.showwarning("Startup Warning", "Teacher data could not be loaded. Teacher details may be missing.")
    # Ensure teachers is an empty dict if missing, though common.py should handle this
    if teachers is None: teachers = {}


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
        # Try different themes if 'clam' isn't ideal on your system
        try:
            style.theme_use("clam") # 'clam', 'alt', 'default', 'classic' are common options
        except tk.TclError:
            print("Clam theme not found, using default.")
            style.theme_use("default")

        # Use fallback colors if system lookup fails or isn't desired
        frame_bg = "#f0f0f0"
        label_fg = "black"
        entry_bg = "white"
        entry_fg = "black"

        style.configure("TFrame", background=frame_bg)
        style.configure("TLabel", background=frame_bg, foreground=label_fg)
        style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg)
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
        # Use the globally loaded USERS dictionary from common.py
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

        # Use theme for consistency
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            style.theme_use("default")

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

        self.mainloop()

    def load_role_frame(self):
        """Creates and displays the frame based on the user's role."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.role == "administrator":
            # Instantiate AdminFrame from admin_view.py
            AdminFrame(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif self.role == "staff":
             # Instantiate StaffFrame from staff_view.py
            StaffFrame(self.content_frame).pack(fill=tk.BOTH, expand=True)
        elif self.role == "student":
             # Instantiate StudentFrame from student_view.py
            if self.student_id:
                # Access global 'students' from common.py for check
                if self.student_id in students:
                    StudentFrame(self.content_frame, self.student_id).pack(fill=tk.BOTH, expand=True)
                else:
                    messagebox.showerror("Error", f"Student ID {self.student_id} not found in student data.")
                    self.logout() # Go back to login
            else:
                messagebox.showerror("Error", "Student ID not found for student login.")
                self.logout() # Go back to login
        else:
            messagebox.showerror("Error", f"Unknown user role: {self.role}")
            self.logout() # Go back to login

    def logout(self):
        """Log out the current user and return to the login screen."""
        self.destroy()
        # Create a new LoginWindow instance
        LoginWindow().mainloop()

# --- Main Execution ---
def main():
    """Start the application by showing the login window."""
    login_window = LoginWindow()
    login_window.mainloop()

if __name__ == "__main__":
    main()