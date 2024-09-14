import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
from PIL import Image
import os

def getImageID(path):
    imagePath = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for imagePaths in imagePath:
        faceImage = Image.open(imagePaths).convert('L')
        faceNP = np.array(faceImage)
        Id = int(os.path.split(imagePaths)[-1].split(".")[1])
        faces.append(faceNP)
        ids.append(Id)
        cv2.imshow("Training", faceNP)
        cv2.waitKey(1)
    return ids, faces

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = "datasets"

    IDs, facedata = getImageID(path)
    recognizer.train(facedata, np.array(IDs))
    recognizer.write("Trainer.yml")
    cv2.destroyAllWindows()
    print("Training Completed............")

if __name__ == "__main__":
    train_model()

