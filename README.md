# Face Recognition Door Unlock System

## Project Description

This project is a **Face Recognition-based Door Unlock System** designed to enhance security and automate access control for door operations. By utilizing a Raspberry Pi 4, a camera module, and a servo motor, the system recognizes authorized personnel and opens the dam door upon successful face recognition. The system leverages OpenCV for face detection and the LBPH (Local Binary Pattern Histogram) algorithm for facial recognition, ensuring accuracy and reliability.

## Features

- **Face Detection**: Uses Haar Cascades to detect faces in real time.
- **Face Recognition**: Employs the LBPH algorithm to recognize authorized users.
- **Servo Motor Control**: The servo motor opens and closes the dam door based on recognition results.
- **Button Activation**: Face recognition is triggered by pressing a button.
- **GPIO Control**: Uses Raspberry Pi GPIO pins to interface with the button and servo motor.

## Hardware Requirements

- Raspberry Pi 4
- Raspberry Pi Camera Module V2
- Servo Motor
- Push Button
- Breadboard and Jumper Wires
- GPIO for button and motor control

## Software Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- Picamera2 (`picamera2`)
- RPi.GPIO (`RPi.GPIO`)
- NumPy

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pyaephyo23/-Face-Recognition-Door-Unlock-System.git

2. **Navigate into the project directory**:

bash
cd face-recognition-dam-door


3. **Install the required libraries:

bash
pip install -r requirements.txt


4. **Connect the hardware (Raspberry Pi, camera module, servo motor, button, etc.).


How to Run
Ensure all hardware is connected properly.
Train the face recognizer using the provided scripts to collect and label images.
Start the face recognition and door control process:
bash
python face_recognition_door.py

Press the button to initiate face recognition.
If the face is recognized, the servo motor will open the dam door.
File Structure

bash
├── datasets/                  # Folder containing the dataset of face images
├── Trainer.yml                # Trained model for face recognition
├── face_recognition_door.py    # Main script for face recognition and door control
├── train_model.py             # Script to train the face recognizer
├── collect_faces.py           # Script to collect face data
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation


License
This project is licensed under the MIT License - see the LICENSE file for details.


OpenCV for facial recognition
Picamera2 for camera interaction
Raspberry Pi for hardware contro
