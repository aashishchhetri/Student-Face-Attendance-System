from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re
import time
import json
import os
import mysql.connector
import cv2
import numpy as np
from datetime import datetime
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

# Class for displaying a digital clock
class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.clock_label = Label(root, font=("Times New Roman", 45, "bold"), background="black", foreground="white")
        self.clock_label.place(relx=1.0, rely=0.0, anchor='ne')
        self.update_clock()

    # Method to update the clock every second
    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

# Main class for the student face detection system
class Student:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Set the window to fullscreen
        self.root.title("Face Recognition Attendance System")

        # Connect to the database
        self.conn = mysql.connector.connect(host='localhost', username='root', password='Chhetri@123', database='face recognition')
        self.cursor = self.conn.cursor()

        self.config_file = "column_widths.json"

        # Create the title frame
        title_frame = Frame(root, bg="black")
        title_frame.pack(side=TOP, fill=X)

        # Back button to close the application
        back_button = Button(title_frame, text="Back", font=("Times New Roman", 20, "bold"), bg="white", fg="black", command=self.back)
        back_button.grid(row=0, column=0, padx=10, pady=5)

        # Title label
        title_lbl = Label(title_frame, text="Student Details", font=("Times New Roman", 45, "bold"), bg="black", fg="white")
        title_lbl.grid(row=0, column=1, padx=10)

        title_frame.columnconfigure(1, weight=1)
        title_lbl.grid_configure(sticky="ew")

        # Create the main frame
        main_frame = Frame(root, bd=2, relief=RIDGE)
        main_frame.pack(fill=BOTH, expand=True)

        # Left and right frames inside the main frame
        left_frame = Frame(main_frame, bd=2, relief=RIDGE)
        left_frame.grid(row=0, column=0, sticky="ns")

        right_frame = Frame(main_frame, bd=2, relief=RIDGE)
        right_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Create student information frame inside the left frame
        student_info_frame = LabelFrame(left_frame, text="Student Information", padx=10, pady=10)
        student_info_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Department selection
        Label(student_info_frame, text="Department:").grid(row=0, column=0, sticky='w')
        self.department_combo = ttk.Combobox(student_info_frame, width=19, state="readonly")
        self.department_combo["value"] = ("Select Department", "Computer Science & Information Technology", "Humanities and Social Science", "Management")
        self.department_combo.current(0)
        self.department_combo.grid(row=0, column=1)
        self.department_combo.bind("<<ComboboxSelected>>", self.update_course_based_on_department)

        # Course selection
        Label(student_info_frame, text="Courses:").grid(row=1, column=0, sticky='w')
        self.courses_combo = ttk.Combobox(student_info_frame, width=19, state="readonly")
        self.courses_combo["value"] = ("Select Course", "BSC CSIT", "BCA", "BIM")
        self.courses_combo.current(0)
        self.courses_combo.grid(row=1, column=1)
        self.courses_combo.bind("<<ComboboxSelected>>", self.update_department_based_on_course)

        # Batch entry
        Label(student_info_frame, text="Batch:").grid(row=2, column=0, sticky='w')
        self.batch_entry = Entry(student_info_frame)
        self.batch_entry.grid(row=2, column=1)

        # Student ID entry
        Label(student_info_frame, text="Student ID:").grid(row=4, column=0, sticky='w')
        self.student_id_entry = Entry(student_info_frame)
        self.student_id_entry.grid(row=4, column=1)

        # Student name entry
        Label(student_info_frame, text="Student Name:").grid(row=5, column=0, sticky='w')
        self.student_name_entry = Entry(student_info_frame)
        self.student_name_entry.grid(row=5, column=1)

        # Roll number entry
        Label(student_info_frame, text="Roll No:").grid(row=6, column=0, sticky='w')
        self.roll_no_entry = Entry(student_info_frame)
        self.roll_no_entry.grid(row=6, column=1)

        # Gender selection
        Label(student_info_frame, text="Gender:").grid(row=7, column=0, sticky='w')
        self.gender_combo = ttk.Combobox(student_info_frame, width=19, state="readonly")
        self.gender_combo["value"] = ("Select Gender", "Male", "Female", "Other")
        self.gender_combo.current(0)
        self.gender_combo.grid(row=7, column=1)

        # Date of birth entry using DateEntry
        Label(student_info_frame, text="DOB:").grid(row=8, column=0, sticky='w')
        self.dob_entry = DateEntry(student_info_frame, width=19, background='red', foreground='white', date_pattern='yyyy/mm/dd')
        self.dob_entry.grid(row=8, column=1)

        # Email entry
        Label(student_info_frame, text="Email:").grid(row=9, column=0, sticky='w')
        self.email_entry = Entry(student_info_frame)
        self.email_entry.grid(row=9, column=1)

        # Phone number entry
        Label(student_info_frame, text="Phone No:").grid(row=10, column=0, sticky='w')
        self.phone_no_entry = Entry(student_info_frame)
        self.phone_no_entry.grid(row=10, column=1)

        # Address entry
        Label(student_info_frame, text="Address:").grid(row=11, column=0, sticky='w')
        self.address_entry = Entry(student_info_frame)
        self.address_entry.grid(row=11, column=1)

        # Capture photo button
        Button(student_info_frame, text="Capture Photo Sample", cursor="hand", command=self.capture_photo).grid(row=12, column=0, columnspan=2, pady=10)

        # Buttons to add, reset, delete, and update student details
        Button(student_info_frame, text="Add New", cursor="hand", command=self.validate_entries).grid(row=13, column=0, pady=10)
        Button(student_info_frame, text="Reset", cursor="hand", command=self.reset_entries).grid(row=13, column=1)
        Button(student_info_frame, text="Delete", cursor="hand", command=self.delete_entry).grid(row=14, column=0, pady=10)
        Button(student_info_frame, text="Update", cursor="hand", command=self.update_entry).grid(row=14, column=1)

        # Create student details frame inside the right frame
        student_details_frame = LabelFrame(right_frame, text="Student Details & Search System", padx=10, pady=10)
        student_details_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Search system by course and student details
        course_search_label = Label(student_details_frame, text="Course:")
        course_search_label.grid(row=0, column=0, sticky='w')
        self.course_search_combo = ttk.Combobox(student_details_frame, state="readonly")
        self.course_search_combo["value"] = ("All", "BSC CSIT", "BCA", "BIM")
        self.course_search_combo.current(0)
        self.course_search_combo.grid(row=0, column=1)
        self.course_search_combo.bind("<<ComboboxSelected>>", self.filter_by_course)

        # Add batch search
        batch_search_label = Label(student_details_frame, text="Batch:")
        batch_search_label.grid(row=0, column=2, sticky='w')
        self.batch_search_combo = ttk.Combobox(student_details_frame, state="readonly")
        self.update_batch_years()  # Initialize the batch years
        self.batch_search_combo.grid(row=0, column=3)
        self.batch_search_combo.bind("<<ComboboxSelected>>", self.filter_by_batch)

        search_by_label = Label(student_details_frame, text="Search By:")
        search_by_label.grid(row=0, column=4, sticky='w')
        self.search_by_combo = ttk.Combobox(student_details_frame, state="readonly")
        self.search_by_combo["value"] = ("Select Option", "Student ID", "Student Name")
        self.search_by_combo.current(0)
        self.search_by_combo.grid(row=0, column=5)

        self.search_entry = Entry(student_details_frame)
        self.search_entry.grid(row=0, column=6)

        search_button = Button(student_details_frame, text="SEARCH", cursor="hand", command=self.search_student)
        search_button.grid(row=0, column=7, padx=10)
        show_all_button = Button(student_details_frame, text="SHOW ALL", cursor="hand", command=self.show_all_students)
        show_all_button.grid(row=0, column=8)

        # Display student details in a table
        self.columns = ("department", "course", "batch", "student_id", "student_name", "roll_no", "gender", "dob", "email", "phone_no", "address")
        self.tree = ttk.Treeview(student_details_frame, columns=self.columns, show='headings')
        self.tree.grid(row=1, column=0, columnspan=9, pady=10, sticky='nsew')

        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())

        self.load_column_widths()

        # Bind events for saving column widths and selecting table items
        self.tree.bind('<<TreeviewColumnMoved>>', self.save_column_widths)
        self.tree.bind('<Configure>', self.save_column_widths)
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        student_details_frame.columnconfigure(0, weight=1)
        student_details_frame.rowconfigure(1, weight=1)

        self.load_students_from_db()

    # Method to dynamically generate batch years
    def update_batch_years(self):
        current_year = datetime.now().year
        if datetime.now().month == 11 and datetime.now().day >= 1:
            current_year += 1
        years = [str(year) for year in range(current_year - 4, current_year + 1)]
        self.batch_search_combo["value"] = ["All"] + years
        self.batch_search_combo.current(0)

    # Update courses based on selected department
    def update_course_based_on_department(self, event):
        department = self.department_combo.get()
        if department == "Computer Science & Information Technology":
            self.courses_combo.set("BSC CSIT")
        elif department == "Humanities and Social Science":
            self.courses_combo.set("BCA")
        elif department == "Management":
            self.courses_combo.set("BIM")
        else:
            self.courses_combo.set("Select Course")

    # Update department based on selected course
    def update_department_based_on_course(self, event):
        course = self.courses_combo.get()
        if course == "BSC CSIT":
            self.department_combo.set("Computer Science & Information Technology")
        elif course == "BCA":
            self.department_combo.set("Humanities and Social Science")
        elif course == "BIM":
            self.department_combo.set("Management")
        else:
            self.department_combo.set("Select Department")

    # Load column widths for the table from a JSON file
    def load_column_widths(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                column_widths = json.load(file)
                for col in self.columns:
                    if col in column_widths:
                        self.tree.column(col, width=column_widths[col])
                    else:
                        self.tree.column(col, width=100)
        else:
            column_widths = {
                "department": 190,
                "course": 70,
                "batch": 40,
                "student_id": 70,
                "student_name": 160,
                "roll_no": 60,
                "gender": 60,
                "dob": 100,
                "email": 170,
                "phone_no": 90,
                "address": 170,
            }
            for col in self.columns:
                if col in column_widths:
                    self.tree.column(col, width=column_widths[col])
                else:
                    self.tree.column(col, width=100)

    # Save column widths to a JSON file
    def save_column_widths(self, event=None):
        column_widths = {col: self.tree.column(col, 'width') for col in self.columns}
        with open(self.config_file, 'w') as file:
            json.dump(column_widths, file)

    # Validate user input before adding a student
    def validate_entries(self):
        if not self.department_combo.get() or self.department_combo.get() == "Select Department":
            messagebox.showerror("Input Error", "Department field is empty.")
            return
        if not self.courses_combo.get() or self.courses_combo.get() == "Select Course":
            messagebox.showerror("Input Error", "Courses field is empty.")
            return
        if not self.batch_entry.get():
            messagebox.showerror("Input Error", "Batch field is empty.")
            return
        if not self.student_id_entry.get():
            messagebox.showerror("Input Error", "Student ID field is empty.")
            return
        if not self.student_name_entry.get():
            messagebox.showerror("Input Error", "Student Name field is empty.")
            return
        if not self.roll_no_entry.get():
            messagebox.showerror("Input Error", "Roll No field is empty.")
            return
        if not self.gender_combo.get() or self.gender_combo.get() == "Select Gender":
            messagebox.showerror("Input Error", "Gender field is empty.")
            return
        if not self.dob_entry.get():
            messagebox.showerror("Input Error", "DOB field is empty.")
            return
        if not self.email_entry.get():
            messagebox.showerror("Input Error", "Email field is empty.")
            return
        if not self.phone_no_entry.get():
            messagebox.showerror("Input Error", "Phone No field is empty.")
            return
        if not self.address_entry.get():
            messagebox.showerror("Input Error", "Address field is empty.")
            return

        #dob_pattern = re.compile(r'^\d{4}/\d{2}/\d{2}$')
        #if not dob_pattern.match(self.dob_entry.get()):
            #messagebox.showerror("Invalid Input", "DOB must be in the format YYYY/MM/DD")
            #return

        year_pattern = re.compile(r'^\d{4}$')
        if not year_pattern.match(self.batch_entry.get()):
            messagebox.showerror("Invalid Input", "Year must be a 4-digit number")
            return

        if not self.student_id_entry.get().isalnum():
            messagebox.showerror("Invalid Input", "Student ID must be alphanumeric (letters and numbers).")

            return

        if not self.roll_no_entry.get().isdigit():
            messagebox.showerror("Invalid Input", "Roll No must be numeric")
            return

        phone_pattern = re.compile(r'^\d{10}$')
        if not phone_pattern.match(self.phone_no_entry.get()):
            messagebox.showerror("Invalid Input", "Phone No must be a 10-digit number")
            return

        self.add_student_to_db()

    # Add a new student to the database
    def add_student_to_db(self):
        try:
            student_data = (
                self.department_combo.get(),
                self.courses_combo.get(),
                self.batch_entry.get(),
                self.student_id_entry.get(),
                self.student_name_entry.get(),
                self.roll_no_entry.get(),
                self.gender_combo.get(),
                self.dob_entry.get(),
                self.email_entry.get(),
                self.phone_no_entry.get(),
                self.address_entry.get()
            )
            query = "INSERT INTO students (department, course, batch, student_id, student_name, roll_no, gender, dob, email, phone_no, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, student_data)
            self.conn.commit()
            self.tree.insert('', 'end', values=student_data)
            messagebox.showinfo("Success", "Student added successfully")
            self.reset_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student to database: {str(e)}")

    # Reset input fields
    def reset_entries(self):
        self.department_combo.current(0)
        self.courses_combo.current(0)
        self.batch_entry.delete(0, END)
        self.student_id_entry.delete(0, END)
        self.student_name_entry.delete(0, END)
        self.roll_no_entry.delete(0, END)
        self.gender_combo.current(0)
        self.dob_entry.set_date(datetime.now())  # Reset date to current date
        self.email_entry.delete(0, END)
        self.phone_no_entry.delete(0, END)
        self.address_entry.delete(0, END)

    # Close the application
    def back(self):
        self.root.destroy()

    # Delete a selected student entry from the database
    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student's details?"):
            student_id = self.tree.item(selected_item)['values'][3]
            try:
                query = "DELETE FROM students WHERE student_id = %s"
                self.cursor.execute(query, (student_id,))
                self.conn.commit()
                self.tree.delete(selected_item)
                messagebox.showinfo("Success", "Student deleted successfully")
                self.reset_entries()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student from database: {str(e)}")

    # Update a selected student entry in the database
    def update_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        if messagebox.askyesno("Confirm Update", "Are you sure you want to update this student's details?"):
            try:
                student_id = self.tree.item(selected_item)['values'][3]  # Correct index for student_id
                student_data = (
                    self.department_combo.get(),
                    self.courses_combo.get(),
                    self.batch_entry.get(),
                    self.student_name_entry.get(),
                    self.roll_no_entry.get(),
                    self.gender_combo.get(),
                    self.dob_entry.get(),
                    self.email_entry.get(),
                    self.phone_no_entry.get(),
                    self.address_entry.get(),
                    student_id
                )
                query = """
                UPDATE students 
                SET department = %s, course = %s, batch = %s, student_name = %s, roll_no = %s, gender = %s, dob = %s, email = %s, phone_no = %s, address = %s
                WHERE student_id = %s
                """
                self.cursor.execute(query, student_data)
                self.conn.commit()
                self.tree.item(selected_item, values=student_data[:-1])
                messagebox.showinfo("Success", "Student updated successfully")
                self.reset_entries()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update student in database: {str(e)}")

    # Capture multiple photos using webcam
    def capture_photo(self):
        student_id = self.student_id_entry.get()
        if not student_id:
            messagebox.showerror("Input Error", "Please enter Student ID before capturing photos.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not access the webcam.")
            return

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        photo_count = 0
        total_photos = 200  # Number of photos to capture

        if not os.path.exists("data"):
            os.makedirs("data")

        while photo_count < total_photos:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture photo from the webcam.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    face = frame[y:y+h, x:x+w]
                    resized_face = cv2.resize(face, (350, 350))  # Resize to 200x200 pixels
                    
                    photo_count += 1
                    save_path = os.path.join("data", f"student_{student_id}_{photo_count}.jpg")
                    cv2.imwrite(save_path, resized_face)  # Save the resized face
                    cv2.imshow("Capturing Photos", resized_face)

            cv2.imshow('Capture Photo - Press Q to Quit', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


    # Select a student entry from the table and populate the input fields
    def select_item(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        student_data = item['values']

        self.department_combo.set(student_data[0])
        self.courses_combo.set(student_data[1])
        self.batch_entry.delete(0, END)
        self.batch_entry.insert(0, student_data[2])
        self.student_id_entry.delete(0, END)
        self.student_id_entry.insert(0, student_data[3])
        self.student_name_entry.delete(0, END)
        self.student_name_entry.insert(0, student_data[4])
        self.roll_no_entry.delete(0, END)
        self.roll_no_entry.insert(0, student_data[5])
        self.gender_combo.set(student_data[6])
        self.dob_entry.set_date(student_data[7])
        self.email_entry.delete(0, END)
        self.email_entry.insert(0, student_data[8])
        self.phone_no_entry.delete(0, END)
        self.phone_no_entry.insert(0, student_data[9])
        self.address_entry.delete(0, END)
        self.address_entry.insert(0, student_data[10])

    # Search for a student based on selected criteria
    def search_student(self):
        search_by = self.search_by_combo.get()
        search_term = self.search_entry.get()

        if search_by == "Select Option" or not search_term:
            messagebox.showerror("Error", "Please select a valid search option and enter a search term")
            return

        try:
            if search_by == "Student ID":
                query = "SELECT * FROM students WHERE student_id = %s"
                self.cursor.execute(query, (search_term,))
            elif search_by == "Student Name":
                query = "SELECT * FROM students WHERE student_name LIKE %s"
                self.cursor.execute(query, ('%' + search_term + '%',))

            rows = self.cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search students in database: {str(e)}")

    # Show all student entries
    def show_all_students(self):
        self.tree.delete(*self.tree.get_children())
        self.load_students_from_db()

    # Filter students by selected course
    def filter_by_course(self, event):
        selected_course = self.course_search_combo.get()
        self.tree.delete(*self.tree.get_children())

        try:
            if selected_course == "All":
                query = "SELECT * FROM students"
                self.cursor.execute(query)
            else:
                query = "SELECT * FROM students WHERE course = %s"
                self.cursor.execute(query, (selected_course,))

            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter students by course in database: {str(e)}")

    # Filter students by selected batch
    def filter_by_batch(self, event):
        selected_batch = self.batch_search_combo.get()
        self.tree.delete(*self.tree.get_children())

        try:
            if selected_batch == "All":
                query = "SELECT * FROM students"
                self.cursor.execute(query)
            else:
                query = "SELECT * FROM students WHERE batch = %s"
                self.cursor.execute(query, (selected_batch,))

            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter students by batch in database: {str(e)}")

    # Get all student details from the table
    def get_all_students(self):
        students = []
        for item in self.tree.get_children():
            students.append(self.tree.item(item, 'values'))
        return students

    # Load student details from the database and display in the table
    def load_students_from_db(self):
        try:
            query = "SELECT * FROM students"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students from database: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    clock = DigitalClock(root)
    root.mainloop()
