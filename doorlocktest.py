import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from libcamera import controls

# Setup GPIO
GPIO.setmode(GPIO.BCM)
servo_pin = 17
button_pin = 18  # Define the GPIO pin for the button
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Setup button as input with a pull-up resistor

# Setup PWM for the servo motor
pwm = GPIO.PWM(servo_pin, 50)  # Set frequency to 50Hz (20ms period)
pwm.start(0)  # Initialize the servo at 0 degrees (closed position)

def set_servo_angle(angle):
    # Convert angle to duty cycle
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)  # Stop the PWM signal

# Load the face detection classifier
face_classifier = cv2.CascadeClassifier('/home/pi/Desktop/raspberry-pi-main/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Desktop/raspberry-pi-main/Trainer.yml')

def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return img, []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))

    return img, roi

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

x, c, d, m = 0, 0, 0, 0

try:
    while True:
        # Wait for the button press
        button_state = GPIO.input(button_pin)
        if button_state == GPIO.LOW:  # Button is pressed
            print("Button Pressed! Starting face recognition...")

            while True:
                # Capture image
                frame = picam2.capture_array()
                image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                image, face = face_detector(image)

                try:
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    result = recognizer.predict(face)
                    if result[1] < 500:
                        confidence = int((1 - (result[1]) / 300) * 100)
                        display_string = f'Confidence: {confidence}%'
                        cv2.putText(image, display_string, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                    if confidence >= 83:
                        cv2.putText(image, "Access Granted", (100, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
                        x += 1
                        if x >= 5:  # Successfully recognized 5 times
                            m = 1
                            set_servo_angle(90)  # Open door
                            time.sleep(5)       # Keep the door open for 5 seconds
                            set_servo_angle(0)   # Close door
                            break
                    else:
                        cv2.putText(image, "Access Denied", (100, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                        c += 1
                except:
                    cv2.putText(image, "No Face Detected", (100, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
                    d += 1

                cv2.imshow('Face Recognition', image)

                if cv2.waitKey(1) == 13:  # Exit if 'Enter' is pressed
                    break

            # After the recognition process, stop the loop until the button is pressed again
            cv2.destroyAllWindows()
            print("Waiting for button press to start recognition again...")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    pwm.stop()
