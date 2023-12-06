import cv2
import face_recognition
import os
import tkinter as tk
from tkinter import messagebox

# Load images and names from the folder
image_folder = "faces"
known_face_encodings = []
known_face_names = []

for filename in os.listdir(image_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        path = os.path.join(image_folder, filename)
        image = face_recognition.load_image_file(path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(os.path.splitext(filename)[0])


cap = cv2.VideoCapture(0)


root = tk.Tk()
root.withdraw()  # Hide the root window

def show_popup(message):
    messagebox.showinfo("Multiple Faces Detected", message)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Check the number of faces detected
    num_faces = len(face_locations)

   
    if num_faces > 1:
        show_popup("More than one face detected! Please ensure only one person is in the frame.")

   
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"
        color = (0, 0, 255)  # Default color is red (BGR format)

       
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            color = (0, 255, 0)  

        
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    
    cv2.imshow('Face Recognition', frame)

    
    if num_faces == 1:
        root.update_idletasks()
        root.update()

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
