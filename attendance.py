import cv2
import face_recognition
import os
import pandas as pd
import time

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

# Load or create the Excel sheet
excel_path = "attendance_sheet.xlsx"
if os.path.exists(excel_path):
    attendance_df = pd.read_excel(excel_path)
else:
    attendance_df = pd.DataFrame(columns=["Name", "Time"])


cap = cv2.VideoCapture(0)


attendance_duration = 60
start_time = time.time()

while (time.time() - start_time) < attendance_duration:
    # Read a frame from the camera
    ret, frame = cap.read()

    
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"
        color = (0, 255, 0)  # Default color is green

        
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            
            if name in attendance_df["Name"].values:
                color = (0, 0, 255) 

                # Display "Already Marked" text
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "Already Marked", (left + 6, bottom - 6), font, 0.5, color, 1)

            else:
                
                new_attendance = pd.DataFrame({"Name": [name], "Time": [time.strftime("%Y-%m-%d %H:%M:%S")]})
                attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)
                attendance_df.to_excel(excel_path, index=False)


        
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

   
    cv2.imshow('Face Recognition', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
