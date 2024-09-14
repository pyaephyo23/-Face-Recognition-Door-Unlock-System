import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls

# Update this path to where you have the haarcascade_frontalface_default.xml file on your Raspberry Pi
face_classifier_path = '/home/pi/Desktop/raspberry-pi-main/haarcascade_frontalface_default.xml'
face_classifier = cv2.CascadeClassifier(face_classifier_path)

id = input("Enter Your ID: ")
id = int(id)

def face_extractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None
    for (x, y, w, h) in faces:
        cropped_face = img[y:y + h, x:x + w]
    return cropped_face

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

count = 0
print("Please look into the camera.")

while True:
    frame = picam2.capture_array()
    if frame is None:
        print("Failed to grab frame.")
        break

    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if face_extractor(image) is not None:
        count += 1
        face = cv2.resize(face_extractor(image), (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        
        #change your file path
        file_name_path = f'/home/pi/Desktop/raspberry-pi-main/datasets/User.{id}.{count}.jpg'
        cv2.imwrite(file_name_path, face)

        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Face Cropper", face)
    else:
        print('Face not found')

    if cv2.waitKey(1) == 13 or count == 10:
        break

picam2.stop()
cv2.destroyAllWindows()
print("Collecting samples complete")

