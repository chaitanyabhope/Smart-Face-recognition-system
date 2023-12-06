import tkinter as tk
from tkinter import ttk
import os
import subprocess

def start_attendance_system():
    root.destroy()  # Close the welcome window
    subprocess.run(["python", "attendance.py"])

def start_exam_system():
    root.destroy()  # Close the welcome window
    subprocess.run(["python", "face.py"])

def close_application():
    root.destroy()

root = tk.Tk()
root.title("Face Recognition System")

# Set the window size
root.geometry("600x400")
root.resizable(False, False)  # Disable window resizing

# Create a style for buttons
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=10)

# Create a welcome message label
welcome_label = tk.Label(root, text="Welcome to the Face Recognition System!", font=("Helvetica", 18))
welcome_label.pack(pady=20)

# Create buttons for attendance, exam, and cancel options
attendance_button = ttk.Button(root, text="1- Attendance System", command=start_attendance_system)
attendance_button.pack(pady=10)

exam_button = ttk.Button(root, text="2- Exam Invigilation System", command=start_exam_system)
exam_button.pack(pady=10)

cancel_button = ttk.Button(root, text="3- Cancel", command=close_application)
cancel_button.pack(pady=10)

# Run the tkinter main loop
root.mainloop()
