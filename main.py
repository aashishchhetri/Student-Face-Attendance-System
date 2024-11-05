from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from student import Student
from teacher import Teacher
from attendance import Attendance
from traindata import Train_Data
import time
from facerecognition import Face_Recognition
import os
import subprocess
import platform

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.clock_label = Label(root, font=("Times New Roman", 45, "bold"), background="black", foreground="white")
        self.clock_label.place(relx=1.0, rely=0.0, anchor='ne')  # Place it at the top right corner

        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

class Face_Detection_System:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Set the window to fullscreen
        self.root.title("Face Recognition Attendance System")

        # Create and place the title label
        title_lbl = Label(root, text="FaceTime Attendance", font=("Times New Roman", 45, "bold"), bg="black", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        # Create a frame to hold the buttons
        button_frame = Frame(root)
        button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Button names
        button_names = ["Student Details","Teacher Details", "Face Recognition", "Attendance", "Train Data", "Photo"]

        # Create and place the buttons in the grid with background images and custom names
        for i in range(6):
            if button_names[i] == "Student Details":
                button = Button(button_frame, text=button_names[i], font=("Times New Roman", 20, "bold"), width=40, height=8, compound="center", cursor="hand2", command=self.student_details)
            elif button_names[i] == "Teacher Details":
                button = Button(button_frame, text=button_names[i], font=("Times New Roman", 20, "bold"), width=40, height=8, compound="center", cursor="hand2", command=self.teacher_details)
            elif button_names[i] == "Face Recognition":
                button = Button(button_frame, text=button_names[i], font=("Times New Roman", 20, "bold"), width=40, height=8, compound="center", cursor="hand2", command=self.face_recognition)
            elif button_names[i] == "Attendance":
                button = Button(button_frame, text=button_names[i], font=("Times New Roman", 20, "bold"), width=40, height=8, compound="center", cursor="hand2", command=self.attendance)
            elif button_names[i] == "Train Data":
                button = Button(button_frame, text=button_names[i], font=("Times New Roman", 20, "bold"), width=40, height=8, compound="center", cursor="hand2", command=self.train_data)
            elif button_names[i] == "Photo":
                button = Button(button_frame, text=button_names[i],  font=("Times New Roman", 20, "bold"), width=40, height=8, compound="center", cursor="hand2", command=self.open_img)    
            else:
                button = Button(button_frame, text=button_names[i], font=("Times New Roman", 20, "bold"), width=40, height=8, compound="center", cursor="hand2")
            button.grid(row=i//3, column=i%3, padx=10, pady=10)

    # Exit button
        exit_button = Button(self.root, text="Exit", font=("Helvetica", 13), bg="white", fg="black", command=self.exit_app)
        exit_button.place(x=1800, y=1000, width=100, height=50)        

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)
        self.clock = DigitalClock(self.new_window)
        
    def teacher_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Teacher(self.new_window)
        self.clock = DigitalClock(self.new_window)
        
    def face_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)
        self.clock = DigitalClock(self.new_window)

    def attendance(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)
        self.clock = DigitalClock(self.new_window)  # Instantiate DigitalClock in the new window  

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train_Data(self.new_window)
        self.clock = DigitalClock(self.new_window)  # Instantiate DigitalClock in the new window

    def open_img(self):
        folder_path = "data"
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", f"The folder '{folder_path}' does not exist.")
            return

        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", folder_path])

    def exit_app(self):
        self.root.quit()        

if __name__ == "__main__":
    root = Tk()
    obj = Face_Detection_System(root)
    root.mainloop()  # main loop is used to run the application, it is an infinite loop