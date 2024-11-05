import cv2
import numpy as np
import mysql.connector
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import csv

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Set the window to fullscreen
        self.root.title("Face Recognition Attendance System")

        # Create and place the title frame
        title_frame = Frame(root, bg="black")
        title_frame.pack(side=TOP, fill=X)

        # Create a "Back" button in the top right corner
        back_button = Button(title_frame, text="Back", font=("Times New Roman", 20, "bold"), bg="white", fg="black", command=self.back)
        back_button.grid(row=0, column=0, padx=10, pady=5)

        # Add title label in the title frame
        title_lbl = Label(title_frame, text="Face Recognition", font=("Times New Roman", 45, "bold"), bg="black", fg="white")
        title_lbl.grid(row=0, column=1, padx=10)

        title_frame.columnconfigure(1, weight=1)
        title_lbl.grid_configure(sticky="ew")

        # Load pre-trained face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Load face recognizer
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        except AttributeError:
            self.recognizer = cv2.createLBPHFaceRecognizer()

        # Check if the classifier.xml file exists
        if os.path.exists('classifier.xml'):
            self.recognizer.read('classifier.xml')
        else:
            messagebox.showerror("Error", "Classifier file not found. Please train the model first.")
            self.root.destroy()
            return

        # Connect to the database
        self.conn = mysql.connector.connect(host='localhost', username='root', password='Chhetri@123', database='face recognition')
        self.cursor = self.conn.cursor()

        # Create the UI components
        self.create_ui()

    def create_ui(self):
        # Create a frame for the camera feed
        self.cam_frame = LabelFrame(self.root, text="Camera Feed", padx=10, pady=10)
        self.cam_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Create a label for the camera feed
        self.cam_label = Label(self.cam_frame)
        self.cam_label.pack()

        # Create a button to start face recognition
        self.recognize_button = Button(self.root, text="Start Face Recognition", command=self.start_recognition, font=("Times New Roman", 20, "bold"), bg="white", fg="black")
        self.recognize_button.pack(pady=20)

    def start_recognition(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Could not access the webcam.")
            return

        self.update_frame(cap)

    def update_frame(self, cap):
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture photo from the webcam.")
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 50:
                # Face is recognized, green rectangle
                label, user_type, details = self.get_user_details(id)
                if details:  # Ensure we have user details
                    self.mark_attendance(details, user_type)  # Pass all details and user type
                rectangle_color = (0, 255, 0)  # Green
            else:
                # Face is not recognized, red rectangle
                label = "Unknown"
                rectangle_color = (0, 0, 255)  # Red

            # Draw the rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), rectangle_color, 2)

            # Display the label above the face
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, rectangle_color, 2)

        # Convert the OpenCV frame (BGR) to PIL Image (RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the label with the captured frame
        self.cam_label.img_tk = img_tk  # Keep a reference
        self.cam_label.config(image=img_tk)

        # Continue updating frames after a short delay
        self.cam_label.after(10, self.update_frame, cap)

    def get_user_details(self, id):
        # Check in students table
        query = """
        SELECT course, student_id, student_name, batch 
        FROM students 
        WHERE student_id = %s
        """
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            course, id, name, batch = result
            label = f"{course}, {id}, {name}, Batch: {batch}"
            details = (id, name, course, batch)
            return label, "Student", details

        # Check in teachers table
        query = "SELECT teacher_name FROM teachers WHERE teacher_id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            name = result[0]
            label = f"{name} (Teacher)"
            # For teachers, we might skip the batch and course, so only return name
            details = (id, name, "N/A", "N/A")
            return label, "Teacher", details

        return "Unknown", None, None

    def mark_attendance(self, details, user_type):
        id, name, course, batch = details
        today_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        # Determine the appropriate file based on user type
        if user_type == "Student":
            attendance_file = "student_attendance.csv"
        elif user_type == "Teacher":
            attendance_file = "teacher_attendance.csv"
        else:
            return  # If neither, do not proceed

        # Check if today's attendance is already marked for this ID
        if os.path.exists(attendance_file):
            with open(attendance_file, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    # Ensure row has the expected 6 columns before accessing elements
                    if len(row) == 6:
                        if row[0] == str(id) and row[4] == today_date:
                            # Attendance already marked today
                            return

        # Mark attendance if not already marked
        with open(attendance_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([id, name, course, batch, today_date, current_time])

    def back(self):
        # Close the current window
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition(root)
    root.mainloop()
