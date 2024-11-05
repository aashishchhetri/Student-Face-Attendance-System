from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
import re  # Import regex module

class Train_Data:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Set the window to fullscreen
        self.root.title("Face Recognition Attendance System")

        # Create and place the title frame
        title_frame = Frame(root, bg="black")
        title_frame.pack(side=TOP, fill=X)

        # Add back button in the title frame
        back_button = Button(title_frame, text="Back", font=("Times New Roman", 20, "bold"), bg="white", fg="black", command=self.back)
        back_button.grid(row=0, column=0, padx=10, pady=5)

        # Add title label in the title frame
        title_lbl = Label(title_frame, text="Train Data", font=("Times New Roman", 45, "bold"), bg="black", fg="white")
        title_lbl.grid(row=0, column=1, padx=10)

        title_frame.columnconfigure(1, weight=1)
        title_lbl.grid_configure(sticky="ew")

        # Create and place a frame in between the title and the "Train Data" button
        middle_frame = Frame(root, bd=2, relief=RIDGE, padx=10, pady=10, bg="gray")
        middle_frame.pack(pady=20, fill=BOTH, expand=True)  # Adjust padding as needed

        # Optional: Add some content to the middle frame (e.g., label, image, etc.)
        middle_label = Label(middle_frame, text="Middle Frame Content", font=("Times New Roman", 20, "bold"), bg="gray", fg="white")
        middle_label.pack(padx=10, pady=10)

        # Add Train Data button below the new middle frame
        train_button = Button(self.root, text="Train Data", command=self.train_classifier, cursor="hand2", font=("Times New Roman", 35, "bold"), bg="red")
        train_button.pack(pady=20)  # You can adjust the padding as needed

    def back(self):
        # Close the current window
        self.root.destroy()

    def train_classifier(self):
        try:
            data_dir = "data"
            path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.jpg') or file.endswith('.png')]

            faces = []
            ids = []

            for image in path:
                try:
                    img = Image.open(image).convert('L')  # Convert image to grayscale
                    imageNp = np.array(img, 'uint8')

                    # Extract ID using regex
                    id_search = re.search(r'(\d+)', os.path.split(image)[1])
                    if id_search:
                        id = int(id_search.group(1))  # Get the first numeric group found
                    else:
                        raise ValueError(f"No valid ID found in filename {image}")

                    faces.append(imageNp)
                    ids.append(id)
                    cv2.imshow("Training", imageNp)
                    cv2.waitKey(1)
                except Exception as e:
                    print(f"Failed to process image {image}: {e}")
                    continue

            ids = np.array(ids)

            # Train the Classifier And save
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            clf.write("classifier.xml")
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training Data Complete")

        except Exception as e:
            cv2.destroyAllWindows()
            messagebox.showerror("Error", f"Training failed: {e}")

if __name__ == "__main__":
    root = Tk()
    obj = Train_Data(root)
    root.mainloop()
