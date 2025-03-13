import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# -----------------------------
# Hard-coded data
# -----------------------------

# Teachers data
teachers = {
    3001: {
        "firstname": "John",
        "surname": "Smith",
        "title": "Mr",
        "contact": "123-456-7890"
    },
    3002: {
        "firstname": "Sarah",
        "surname": "Connor",
        "title": "Ms",
        "contact": "987-654-3210"
    }
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

# Students data
students = {
    101908: {
        "firstname": "Maddi",
        "surname": "Gascar",
        "gender": "Female",
        "year_level": 9,
        "house": "Bradman",
        "dob": "27/06/2005",
        "activity_id": 2001
    },
    101920: {
        "firstname": "Laura",
        "surname": "Norder",
        "gender": "Female",
        "year_level": 11,
        "house": "Chisholm",
        "dob": "31/07/2002",
        "activity_id": 2002
    },
    136111: {
        "firstname": "Don",
        "surname": "Keigh",
        "gender": "Male",
        "year_level": 12,
        "house": "Lawson",
        "dob": "14/06/2003",
        "activity_id": 2002
    },
    136179: {
        "firstname": "Jim",
        "surname": "Pansey",
        "gender": "Male",
        "year_level": 12,
        "house": "Sturt",
        "dob": "06/10/2002",
        "activity_id": 2001
    }
}


class LoginWindow:
    """
    A simple login window that checks for a hard-coded username/password
    and then opens the main window if correct.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Login Screen")

        self.username_label = ttk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.username_entry = ttk.Entry(self.master)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = ttk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.password_entry = ttk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = ttk.Button(self.master, text="Login", command=self.check_credentials)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Hard-coded credentials for demonstration
        self.valid_username = "admin"
        self.valid_password = "admin"

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.valid_username and password == self.valid_password:
            # Destroy login window
            self.master.destroy()
            # Open main application window
            open_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password.")


class MainWindow:
    """
    The main window that displays a list of students and shows
    their extracurricular activity details when selected.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Student Extracurricular Program")

        # Frame for list of students
        self.left_frame = ttk.Frame(self.master, padding="10 10 10 10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for student details
        self.right_frame = ttk.Frame(self.master, padding="10 10 10 10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Label for list
        ttk.Label(self.left_frame, text="Select a student:").pack(anchor=tk.W)

        # Listbox to display students
        self.student_listbox = tk.Listbox(self.left_frame, height=10, width=30)
        self.student_listbox.pack(fill=tk.BOTH, expand=True)

        # Populate listbox
        for student_id, info in students.items():
            display_name = f"{student_id} - {info['firstname']} {info['surname']}"
            self.student_listbox.insert(tk.END, display_name)

        # Bind selection event
        self.student_listbox.bind("<<ListboxSelect>>", self.show_student_activity)

        # Student details labels
        self.details_label = ttk.Label(self.right_frame, text="Activity Details", font=("Arial", 14, "bold"))
        self.details_label.pack(anchor=tk.N)

        self.activity_info_label = ttk.Label(self.right_frame, text="", justify=tk.LEFT)
        self.activity_info_label.pack(anchor=tk.NW, pady=10)

    def show_student_activity(self, event):
        """When a student is selected in the list, display their activity details."""
        selection = self.student_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        student_entry = self.student_listbox.get(index)
        # Extract the student_id from the listbox entry (split by space or hyphen).
        student_id_str = student_entry.split()[0]
        student_id = int(student_id_str)

        student_data = students[student_id]
        activity_id = student_data["activity_id"]
        activity_data = activities.get(activity_id, {})

        # Build a string to display
        info_text = (
            f"Student: {student_data['firstname']} {student_data['surname']}\n"
            f"Year Level: {student_data['year_level']}\n"
            f"House: {student_data['house']}\n\n"
            f"Enrolled Activity: {activity_data.get('activity', 'N/A')}\n"
            f"Location: {activity_data.get('location', 'N/A')}\n"
            f"Days: {activity_data.get('days', 'N/A')}  |  Time: {activity_data.get('time', 'N/A')}\n"
            f"Cost: ${activity_data.get('cost', 'N/A')}\n"
            f"Start Date: {activity_data.get('start_date', 'N/A')}  |  End Date: {activity_data.get('end_date', 'N/A')}\n"
        )

        self.activity_info_label.config(text=info_text)


def open_main_window():
    """
    Create a new Tk instance for the main application window.
    """
    main_root = tk.Tk()
    MainWindow(main_root)
    main_root.mainloop()


def main():
    # Create the login window
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
