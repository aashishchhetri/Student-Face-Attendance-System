from tkinter import *
from tkinter import ttk, messagebox
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

# Main class for the teacher face detection system
class Teacher:
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
        title_lbl = Label(title_frame, text="Teacher Details", font=("Times New Roman", 45, "bold"), bg="black", fg="white")
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

        # Create teacher information frame inside the left frame
        teacher_info_frame = LabelFrame(left_frame, text="Teacher Information", padx=10, pady=10)
        teacher_info_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Teacher ID entry
        Label(teacher_info_frame, text="Teacher ID:").grid(row=0, column=0, sticky='w')
        self.teacher_id_entry = Entry(teacher_info_frame)
        self.teacher_id_entry.grid(row=0, column=1)

        # Teacher name entry
        Label(teacher_info_frame, text="Teacher Name:").grid(row=1, column=0, sticky='w')
        self.teacher_name_entry = Entry(teacher_info_frame)
        self.teacher_name_entry.grid(row=1, column=1)

        # Gender selection
        Label(teacher_info_frame, text="Gender:").grid(row=2, column=0, sticky='w')
        self.gender_combo = ttk.Combobox(teacher_info_frame, width=19, state="readonly")
        self.gender_combo["value"] = ("Select Gender", "Male", "Female", "Other")
        self.gender_combo.current(0)
        self.gender_combo.grid(row=2, column=1)

        # Date of birth entry using DateEntry
        Label(teacher_info_frame, text="DOB:").grid(row=3, column=0, sticky='w')
        self.dob_entry = DateEntry(teacher_info_frame, width=19, background='black', foreground='white', date_pattern='yyyy/mm/dd')
        self.dob_entry.grid(row=3, column=1)

        # Email entry
        Label(teacher_info_frame, text="Email:").grid(row=4, column=0, sticky='w')
        self.email_entry = Entry(teacher_info_frame)
        self.email_entry.grid(row=4, column=1)

        # Phone number entry
        Label(teacher_info_frame, text="Phone No:").grid(row=5, column=0, sticky='w')
        self.phone_no_entry = Entry(teacher_info_frame)
        self.phone_no_entry.grid(row=5, column=1)

        # Address entry
        Label(teacher_info_frame, text="Address:").grid(row=6, column=0, sticky='w')
        self.address_entry = Entry(teacher_info_frame)
        self.address_entry.grid(row=6, column=1)

        # Capture photo button
        Button(teacher_info_frame, text="Capture Photo Sample", cursor="hand", command=self.capture_photo).grid(row=7, column=0, columnspan=2, pady=10)

        # Buttons to add, reset, delete, and update teacher details
        Button(teacher_info_frame, text="Add New", cursor="hand", command=self.validate_entries).grid(row=8, column=0, pady=10)
        Button(teacher_info_frame, text="Reset", cursor="hand", command=self.reset_entries).grid(row=8, column=1)
        Button(teacher_info_frame, text="Delete", cursor="hand", command=self.delete_entry).grid(row=9, column=0, pady=10)
        Button(teacher_info_frame, text="Update", cursor="hand", command=self.update_entry).grid(row=9, column=1)

        # Create teacher details frame inside the right frame
        teacher_details_frame = LabelFrame(right_frame, text="Teacher Details & Search System", padx=10, pady=10)
        teacher_details_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Search system by teacher details
        search_by_label = Label(teacher_details_frame, text="Search By:")
        search_by_label.grid(row=0, column=0, sticky='w')
        self.search_by_combo = ttk.Combobox(teacher_details_frame, state="readonly")
        self.search_by_combo["value"] = ("Select Option", "Teacher ID", "Teacher Name")
        self.search_by_combo.current(0)
        self.search_by_combo.grid(row=0, column=1)

        self.search_entry = Entry(teacher_details_frame)
        self.search_entry.grid(row=0, column=2)

        search_button = Button(teacher_details_frame, text="SEARCH", cursor="hand", command=self.search_teacher)
        search_button.grid(row=0, column=3, padx=10)
        show_all_button = Button(teacher_details_frame, text="SHOW ALL", cursor="hand", command=self.show_all_teachers)
        show_all_button.grid(row=0, column=4)

        # Display teacher details in a table
        self.columns = ("teacher_id", "teacher_name", "gender", "dob", "email", "phone_no", "address")
        self.tree = ttk.Treeview(teacher_details_frame, columns=self.columns, show='headings')
        self.tree.grid(row=1, column=0, columnspan=5, pady=10, sticky='nsew')

        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())

        self.load_column_widths()

        # Bind events for saving column widths and selecting table items
        self.tree.bind('<<TreeviewColumnMoved>>', self.save_column_widths)
        self.tree.bind('<Configure>', self.save_column_widths)
        self.tree.bind("<<TreeviewSelect>>", self.select_item)

        teacher_details_frame.columnconfigure(0, weight=1)
        teacher_details_frame.rowconfigure(1, weight=1)

        self.load_teachers_from_db()

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
                "teacher_id": 70,
                "teacher_name": 160,
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

    # Validate user input before adding a teacher
    def validate_entries(self):
        if not self.teacher_id_entry.get():
            messagebox.showerror("Input Error", "Teacher ID field is empty.")
            return
        if not self.teacher_name_entry.get():
            messagebox.showerror("Input Error", "Teacher Name field is empty.")
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

        if not self.teacher_id_entry.get().isdigit():
            messagebox.showerror("Invalid Input", "Teacher ID must be numeric")
            return

        phone_pattern = re.compile(r'^\d{10}$')
        if not phone_pattern.match(self.phone_no_entry.get()):
            messagebox.showerror("Invalid Input", "Phone No must be a 10-digit number")
            return

        self.add_teacher_to_db()

    # Add a new teacher to the database
    def add_teacher_to_db(self):
        try:
            teacher_data = (
                self.teacher_id_entry.get(),
                self.teacher_name_entry.get(),
                self.gender_combo.get(),
                self.dob_entry.get(),
                self.email_entry.get(),
                self.phone_no_entry.get(),
                self.address_entry.get()
            )
            query = "INSERT INTO teachers (teacher_id, teacher_name, gender, dob, email, phone_no, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, teacher_data)
            self.conn.commit()
            self.tree.insert('', 'end', values=teacher_data)
            messagebox.showinfo("Success", "Teacher added successfully")
            self.reset_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add teacher to database: {str(e)}")

    # Reset input fields
    def reset_entries(self):
        self.teacher_id_entry.delete(0, END)
        self.teacher_name_entry.delete(0, END)
        self.gender_combo.current(0)
        self.dob_entry.set_date(datetime.now())  # Reset date to current date
        self.email_entry.delete(0, END)
        self.phone_no_entry.delete(0, END)
        self.address_entry.delete(0, END)

    # Close the application
    def back(self):
        self.root.destroy()

    # Delete a selected teacher entry from the database
    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this teacher's details?"):
            teacher_id = self.tree.item(selected_item)['values'][0]
            try:
                query = "DELETE FROM teachers WHERE teacher_id = %s"
                self.cursor.execute(query, (teacher_id,))
                self.conn.commit()
                self.tree.delete(selected_item)
                messagebox.showinfo("Success", "Teacher deleted successfully")
                self.reset_entries()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete teacher from database: {str(e)}")

    # Update a selected teacher entry in the database
    def update_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        if messagebox.askyesno("Confirm Update", "Are you sure you want to update this teacher's details?"):
            try:
                teacher_id = self.tree.item(selected_item)['values'][0]  # Correct index for teacher_id
                teacher_data = (
                    self.teacher_name_entry.get(),
                    self.gender_combo.get(),
                    self.dob_entry.get(),
                    self.email_entry.get(),
                    self.phone_no_entry.get(),
                    self.address_entry.get(),
                    teacher_id
                )
                query = """
                UPDATE teachers 
                SET teacher_name = %s, gender = %s, dob = %s, email = %s, phone_no = %s, address = %s
                WHERE teacher_id = %s
                """
                self.cursor.execute(query, teacher_data)
                self.conn.commit()
                self.tree.item(selected_item, values=(teacher_id, *teacher_data[:-1]))
                messagebox.showinfo("Success", "Teacher updated successfully")
                self.reset_entries()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update teacher in database: {str(e)}")

    # Capture multiple photos using webcam
    def capture_photo(self):
        teacher_id = self.teacher_id_entry.get()
        if not teacher_id:
            messagebox.showerror("Input Error", "Please enter Teacher ID before capturing photos.")
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
                    resized_face = cv2.resize(face, (350, 350))
                
                photo_count += 1
                save_path = os.path.join("data", f"teacher_{teacher_id}_{photo_count}.jpg")
                cv2.imwrite(save_path, frame)
                cv2.imshow("Capturing Photos", frame)

            cv2.imshow('Capture Photo - Press Q to Quit', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # Select a teacher entry from the table and populate the input fields
    def select_item(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item)
        teacher_data = item['values']

        self.teacher_id_entry.delete(0, END)
        self.teacher_id_entry.insert(0, teacher_data[0])
        self.teacher_name_entry.delete(0, END)
        self.teacher_name_entry.insert(0, teacher_data[1])
        self.gender_combo.set(teacher_data[2])
        self.dob_entry.set_date(teacher_data[3])
        self.email_entry.delete(0, END)
        self.email_entry.insert(0, teacher_data[4])
        self.phone_no_entry.delete(0, END)
        self.phone_no_entry.insert(0, teacher_data[5])
        self.address_entry.delete(0, END)
        self.address_entry.insert(0, teacher_data[6])

    # Search for a teacher based on selected criteria
    def search_teacher(self):
        search_by = self.search_by_combo.get()
        search_term = self.search_entry.get()

        if search_by == "Select Option" or not search_term:
            messagebox.showerror("Error", "Please select a valid search option and enter a search term")
            return

        try:
            if search_by == "Teacher ID":
                query = "SELECT * FROM teachers WHERE teacher_id = %s"
                self.cursor.execute(query, (search_term,))
            elif search_by == "Teacher Name":
                query = "SELECT * FROM teachers WHERE teacher_name LIKE %s"
                self.cursor.execute(query, ('%' + search_term + '%',))

            rows = self.cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search teachers in database: {str(e)}")

    # Show all teacher entries
    def show_all_teachers(self):
        self.tree.delete(*self.tree.get_children())
        self.load_teachers_from_db()

    # Get all teacher details from the table
    def get_all_teachers(self):
        teachers = []
        for item in self.tree.get_children():
            teachers.append(self.tree.item(item, 'values'))
        return teachers

    # Load teacher details from the database and display in the table
    def load_teachers_from_db(self):
        try:
            query = "SELECT * FROM teachers"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load teachers from database: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    obj = Teacher(root)
    clock = DigitalClock(root)
    root.mainloop()
