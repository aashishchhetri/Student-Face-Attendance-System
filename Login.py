from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # For adding images if needed
from main import Face_Detection_System  # Import the main function directly

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("925x500+300+200")
        self.root.resizable(False, False)  # Disable resizing

        # Background Color
        self.root.configure(bg="black")

        # Create a Frame for Login Form
        login_frame = Frame(self.root, bg="black")
        login_frame.place(x=250, y=70, width=400, height=350)

        # Title for the Frame
        title = Label(login_frame, text="Login", font=("Helvetica", 30, "bold"), bg="black", fg="white")
        title.place(x=150, y=30)

        # Username Label and Entry
        user_label = Label(login_frame, text="Username", font=("Helvetica", 15), bg="black", fg="white")
        user_label.place(x=50, y=100)
        self.username_entry = Entry(login_frame, font=("Helvetica", 15), bg="black", border=0, width=25)
        self.username_entry.place(x=50, y=130, width=300, height=35)

        # Password Label and Entry
        pass_label = Label(login_frame, text="Password", font=("Helvetica", 15), bg="black", fg="white")
        pass_label.place(x=50, y=180)
        self.password_entry = Entry(login_frame, font=("Helvetica", 15), bg="black", border=0, width=25, show="*")
        self.password_entry.place(x=50, y=210, width=300, height=35)

        # Login Button
        login_button = Button(login_frame, text="Login", font=("Helvetica", 17, "bold"), bg="white", fg="black", command=self.login)
        login_button.place(x=150, y=270, width=100, height=40)

        # Exit button
        exit_button = Button(self.root, text="Exit", font=("Helvetica", 13), bg="white", fg="black", command=self.exit_app)
        exit_button.place(x=850, y=450, width=70, height=35)

    def login(self):
        # Retrieve the input from username and password fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simple validation (replace this with real validation)
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login Success", "Welcome!")

            # Open a new window for the main system (Toplevel)
            self.new_window = Toplevel(self.root)
            self.app = Face_Detection_System(self.new_window)

            # Close the login window after opening the new window
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def exit_app(self):
        self.root.quit()

    def login(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Detection_System(self.new_window)    


if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()
