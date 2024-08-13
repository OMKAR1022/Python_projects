import cv2
import mysql.connector
import base64
import face_recognition
import numpy as np

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysql@123",
    database="testing"
)

# Create a face recognition model
model = face_recognition.models.FaceNetModel()

# Capture images from laptop camera
camera = cv2.VideoCapture(0)
similarity_threshold = 0.5  # Adjust this threshold for matching

# Load the stored faces and labels from the database
cursor = mydb.cursor()
cursor.execute("SELECT name, image FROM om")
results = cursor.fetchall()

# Prepare the training data
known_faces = []
known_face_labels = []

for name, image_base64 in results:
    if image_base64 is not None:
        # Decode the stored image from base64 format
        image_bytes = base64.b64decode(image_base64)

        # Convert the image to numpy array
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)

        # Decode the image array into OpenCV format
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Convert the image to RGB format for face recognition
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect face locations in the image
        face_locations = face_recognition.face_locations(image_rgb, model="hog")

        if len(face_locations) == 1:
            # Encode the face and store the face encoding and label
            face_encoding = model.get_face_embedding(image_rgb, face_locations)[0]
            known_faces.append(face_encoding)
            known_face_labels.append(name)
        else:
            print("No face or multiple faces found in the image!")

while True:
    # Read frame from the camera
    ret, frame = camera.read()

    # Convert the frame to RGB format for face recognition
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations in the frame
    face_locations = face_recognition.face_locations(frame_rgb, model="hog")

    for (top, right, bottom, left) in face_locations:
        # Extract detected face region
        face = frame[top:bottom, left:right]

        # Resize the detected face image to match the size of known faces
        face_resized = cv2.resize(face, (160, 160))

        # Convert the detected face to RGB format for face recognition
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)

        # Encode the face
        face_encoding = model.get_face_embedding(face_rgb)[0]

        if len(known_faces) == 0 or len(known_faces) != len(known_face_labels):
            # No known faces available or mismatch between faces and labels
            matched_label = "Unknown"
            print("No known faces available in the database!")
        else:
            # Calculate the face distance between the detected face and known faces
            face_distances = face_recognition.face_distance(known_faces, face_encoding)

            if len(face_distances) == 0:
                # No faces detected
                matched_label = "Unknown"
                print("No faces detected!")
            else:
                best_match_index = np.argmin(face_distances)

                if best_match_index >= len(known_faces):
                    # Invalid best_match_index
                    matched_label = "Unknown"
                    print("Invalid best_match_index!")
                else:
                    face_distance = face_distances[best_match_index]

                    if face_distance < similarity_threshold:
                        matched_label = known_face_labels[best_match_index]
                        print("Match found! Image is in the database: {}".format(matched_label))
                    else:
                        matched_label = "Unknown"
                        print("No match found!")

        # Draw a rectangle around the detected face and display the label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, matched_label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Camera', frame)

    # Exit loop on pressing 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
