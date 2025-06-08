import sys
import os
import re
import time
import random
import cv2
import numpy as np
import pyttsx3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer

# Define image list
image_list = [
    "emergency.jpg",
    "bottle.jpg",
    "fan.PNG",
    "food.jpg",
    "washroom.jpg",
    "outdoor.jpg"
]

# Generate HTML for images
def generate_image_html(image_name):
    return f'<html><body><img src="{image_name}" style="width: 50px; height: 50px;"></body></html>'

letRowBold = [generate_image_html(img) for img in image_list]

# Face and eye cascades
face_cascade = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarCascades/haarcascade_eye_tree_eyeglasses.xml')

# Video capture
cap = cv2.VideoCapture(0)

# Eye detection variables
bothEyesClosedStart = False
bothEyesClosedStartTime = 0
bothFirst = 0

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to extract image name from HTML
def extract_image_name(html_code):
    match = re.search(r'src="([^"]+)"', html_code)
    if match:
        image_path = match.group(1)
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        return image_name
    else:
        return "Unknown"

# Function to handle text-to-speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Main Window class
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("EyeToText Translator")
        MainWindow.resize(632, 482)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 632, 482))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("EyeToText Translator")
        self.textBrowser.setHtml(letRowBold[0])

# Function to update the displayed image
def update_image():
    global currentImageIndex, ui
    currentImageIndex = (currentImageIndex + 1) % len(letRowBold)
    ui.textBrowser.setHtml(letRowBold[currentImageIndex])

# Function to handle blink detection
def tick():
    global bothEyesClosedStart, bothEyesClosedStartTime, bothFirst, currentImageIndex

    ret, img = cap.read()
    if not ret:
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 1:
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            left_eye_region = roi_gray[:, :w//2]
            right_eye_region = roi_gray[:, w//2:]

            left_eye = eye_cascade.detectMultiScale(left_eye_region)
            right_eye = eye_cascade.detectMultiScale(right_eye_region)

            # Both eyes closed
            if len(left_eye) == 0 and len(right_eye) == 0:
                if not bothEyesClosedStart:
                    bothEyesClosedStartTime = time.time()
                    bothEyesClosedStart = True
                elif time.time() - bothEyesClosedStartTime > 0.75 and bothFirst == 0:
                    bothFirst = 1
                    selected_image_name = extract_image_name(letRowBold[currentImageIndex])
                    print(f"Selected Image: {selected_image_name}")
                    text_to_speech(selected_image_name)
            else:
                bothFirst = 0
                bothEyesClosedStart = False

    cv2.imshow('BlinkToText Video Feed', img)
    if cv2.waitKey(1) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    currentImageIndex = 0
    timer = QTimer()
    timer.timeout.connect(tick)
    timer.start(100)

    image_timer = QTimer()
    image_timer.timeout.connect(update_image)
    image_timer.start(4000)

    sys.exit(app.exec_())
