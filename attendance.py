import csv
import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry  # Importing DateEntry for date selection

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Full-screen mode
        self.root.title("Face Recognition Attendance System")

        # Create and place the title label
        title_frame = Frame(self.root, bd=2, relief=RIDGE, bg="black")
        title_frame.pack(side=TOP, fill=X)

        # Back button
        back_button = Button(title_frame, text="Back", command=self.back, font=("Times New Roman", 25, "bold"), bg="white", fg="black")
        back_button.pack(side=LEFT, padx=10, pady=10)

        title_lbl = Label(title_frame, text="Attendance Management", font=("Times New Roman", 45, "bold"), bg="black", fg="white")
        title_lbl.pack(side=LEFT, padx=450, pady=10)

        # Radio buttons to switch between Student and Teacher attendance
        switch_frame = Frame(self.root, bd=2, relief=RIDGE)
        switch_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        self.attendance_type = StringVar(value="student")
        student_radio = Radiobutton(switch_frame, text="Student Attendance", variable=self.attendance_type, value="student",
                                    font=("Times New Roman", 20, "bold"), command=self.switch_attendance_type)
        teacher_radio = Radiobutton(switch_frame, text="Teacher Attendance", variable=self.attendance_type, value="teacher",
                                    font=("Times New Roman", 20, "bold"), command=self.switch_attendance_type)

        student_radio.pack(side=LEFT, padx=10, pady=5)
        teacher_radio.pack(side=LEFT, padx=10, pady=5)

        # Frame for the details and search
        details_frame = Frame(self.root, bd=2, relief=RIDGE, padx=10, pady=10)
        details_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Search system by course, batch, and date for students
        self.course_label = Label(details_frame, text="Course:", font=("Times New Roman", 20, "bold"))
        self.course_label.grid(row=0, column=0, padx=20, pady=5, sticky=W)
        self.course_combo = ttk.Combobox(details_frame, font=("Times New Roman", 15, "bold"), state="readonly")
        self.course_combo["value"] = ("All", "BSC CSIT", "BCA", "BIM")
        self.course_combo.current(0)
        self.course_combo.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        self.batch_label = Label(details_frame, text="Batch:", font=("Times New Roman", 20, "bold"))
        self.batch_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        self.batch_combo = ttk.Combobox(details_frame, font=("Times New Roman", 15, "bold"), state="readonly")
        self.batch_combo["value"] = self.get_batch_years()
        self.batch_combo.current(0)
        self.batch_combo.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Date search option
        date_label = Label(details_frame, text="Date:", font=("Times New Roman", 20, "bold"))
        date_label.grid(row=0, column=4, padx=10, pady=5, sticky=W)
        self.date_entry = DateEntry(details_frame, font=("Times New Roman", 15, "bold"), width=12, background="black", foreground="white", borderwidth=2, year=datetime.now().year)
        self.date_entry.grid(row=0, column=5, padx=10, pady=5, sticky=W)

        search_button = Button(details_frame, text="SEARCH", command=self.search_attendance, font=("Times New Roman", 15, "bold"), bg="white", fg="black")
        search_button.grid(row=0, column=6, padx=10, pady=5, sticky=W)

        # Attendance Table Frame
        table_frame = Frame(details_frame, bd=2, relief=RIDGE)
        table_frame.grid(row=1, column=0, columnspan=7, sticky='nsew')  # Use grid and set it to expand

        # Configure grid for resizing
        details_frame.grid_rowconfigure(1, weight=1)  # Row 1 (table frame) expands
        details_frame.grid_columnconfigure(0, weight=1)  # Column 0 (table frame) expands

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(table_frame, columns=("id", "name", "course", "batch", "date", "time"), 
                                             xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        self.attendance_table.pack(fill=BOTH, expand=1)

        # New Frame for Export Button
        button_frame = Frame(self.root)
        button_frame.pack(side=BOTTOM, fill=X, padx=20, pady=10)

        # Button to export attendance
        export_button = Button(button_frame, text="EXPORT", command=self.export_attendance, font=("Times New Roman", 25, "bold"), bg="white", fg="black")
        export_button.pack(side=TOP, padx=10)

        # Set initial values and load data
        self.switch_attendance_type()

    def switch_attendance_type(self):
        """Switch between student and teacher attendance"""
        if self.attendance_type.get() == "teacher":
            # Hide the course and batch for teacher attendance, show only date
            self.course_label.grid_remove()
            self.course_combo.grid_remove()
            self.batch_label.grid_remove()
            self.batch_combo.grid_remove()

            # Change columns for teacher attendance (ID, Name, Date, Time)
            self.attendance_table["columns"] = ("id", "name", "course", "batch", "date", "time")
            self.attendance_table.heading("id", text="ID")
            self.attendance_table.heading("name", text="Name")
            self.attendance_table.heading("course", text="Course")
            self.attendance_table.heading("batch", text="Batch")
            self.attendance_table.heading("date", text="Date")
            self.attendance_table.heading("time", text="Time")

            self.attendance_table.column("id", width=200)
            self.attendance_table.column("name", width=650)
            self.attendance_table.column("course", width=500)
            self.attendance_table.column("batch", width=450)
            self.attendance_table.column("date", width=450)
            self.attendance_table.column("time", width=450)

            # Load teacher attendance data
            self.load_attendance_data("teacher_attendance.csv")
        else:
            # Show course and batch fields for student attendance
            self.course_label.grid(row=0, column=0, padx=20, pady=5, sticky=W)
            self.course_combo.grid(row=0, column=1, padx=10, pady=5, sticky=W)
            self.batch_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
            self.batch_combo.grid(row=0, column=3, padx=10, pady=5, sticky=W)

            # Change columns for student attendance (ID, Name, Course, Batch, Date, Time)
            self.attendance_table["columns"] = ("id", "name", "course", "batch", "date", "time")
            self.attendance_table.heading("id", text="ID")
            self.attendance_table.heading("name", text="Name")
            self.attendance_table.heading("course", text="Course")
            self.attendance_table.heading("batch", text="Batch")
            self.attendance_table.heading("date", text="Date")
            self.attendance_table.heading("time", text="Time")

            self.attendance_table.column("id", width=200)
            self.attendance_table.column("name", width=650)
            self.attendance_table.column("course", width=500)
            self.attendance_table.column("batch", width=450)
            self.attendance_table.column("date", width=450)
            self.attendance_table.column("time", width=450)

            # Load student attendance data
            self.load_attendance_data("student_attendance.csv")

    def get_batch_years(self):
        current_year = datetime.now().year
        return ["All"] + [str(year) for year in range(current_year - 4, current_year + 1)]

    def load_attendance_data(self, filename):
        """Load attendance data based on the selected mode"""
        self.attendance_table.delete(*self.attendance_table.get_children())
        if os.path.exists(filename):
            with open(filename, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.attendance_table.insert("", END, values=row)
        else:
            messagebox.showwarning("Warning", f"Attendance file '{filename}' not found!")

    def search_attendance(self):
        """Search attendance based on course, batch, and date for students; or just by date for teachers"""
        selected_date = self.date_entry.get_date().strftime("%Y-%m-%d")  # Get selected date

        if self.attendance_type.get() == "teacher":
            # Search teacher attendance by date only
            filename = "teacher_attendance.csv"
            self.attendance_table.delete(*self.attendance_table.get_children())
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        date = row[2]
                        if date == selected_date:
                            self.attendance_table.insert("", END, values=row)
            else:
                messagebox.showwarning("Warning", "Teacher attendance file not found!")
        else:
            # Search student attendance by course, batch, and date
            selected_course = self.course_combo.get()
            selected_batch = self.batch_combo.get()

            filename = "student_attendance.csv"
            self.attendance_table.delete(*self.attendance_table.get_children())
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        course, batch, date = row[2], row[3], row[4]
                        if (selected_course == "All" or course == selected_course) and (selected_batch == "All" or batch == selected_batch) and date == selected_date:
                            self.attendance_table.insert("", END, values=row)
            else:
                messagebox.showwarning("Warning", "Student attendance file not found!")

    def export_attendance(self):
        files = [('CSV File', '*.csv'), ('All Files', '*.*')]
        file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
        if file:
            try:
                with open(file, "w", newline='') as f:
                    writer = csv.writer(f)
                    for row in self.attendance_table.get_children():
                        row_data = self.attendance_table.item(row)['values']
                        writer.writerow(row_data)
                messagebox.showinfo("Success", "Attendance data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting data: {str(e)}")

    def back(self):
        self.root.destroy()  # This will close the current window

if __name__ == "__main__":
    root = Tk()
    app = Attendance(root)
    root.mainloop()
