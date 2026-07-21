# Hand Gesture Based Brightness Control Using OpenCV and MediaPipe

## Overview

Hand Gesture Based Brightness Control is a Computer Vision project that allows users to control their system's screen brightness using hand gestures captured through a webcam. The application detects the distance between the thumb and index finger in real time and maps it to the screen brightness level.

This project demonstrates the practical use of OpenCV, MediaPipe, and Human-Computer Interaction (HCI) techniques to create a touch-free user interface.

---

## Features

* Real-time hand tracking
* Gesture-based brightness control
* Webcam integration
* Touch-free interaction
* Lightweight and responsive
* Easy to extend for other gesture-controlled applications

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Screen Brightness Control

---

## Project Workflow

1. Capture live video from the webcam.
2. Detect the user's hand using MediaPipe.
3. Identify the thumb tip and index finger tip landmarks.
4. Calculate the distance between the two fingertips.
5. Map the distance to a brightness range.
6. Adjust the screen brightness dynamically.
7. Continuously update the brightness in real time.

---

## Hand Landmarks Used

| Landmark | Description      |
| -------- | ---------------- |
| 4        | Thumb Tip        |
| 8        | Index Finger Tip |

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/HandBrightnessControl.git
cd HandBrightnessControl
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Project

```bash
python brightness_control.py
```

---

## Requirements

```text
opencv-contrib-python==4.10.0.84
mediapipe==0.10.14
numpy==1.26.4
screen-brightness-control==0.27.2
```

---

## System Requirements

### Hardware

* Webcam
* Computer/Laptop

### Software

* Python 3.x
* Windows Operating System

---

## Advantages

* Contactless interaction
* Improved accessibility
* Demonstrates practical computer vision concepts
* Can be expanded into larger gesture-control systems

---

## Limitations

* Requires proper lighting conditions
* Accuracy depends on webcam quality
* Primarily tested on Windows systems
* Multiple hands may affect detection accuracy

---

## Future Enhancements

* Volume control using hand gestures
* Media playback controls
* Mouse cursor control
* Multi-hand gesture recognition
* Smart home device integration
* Gesture-based application launcher

---

## Applications

* Human-Computer Interaction (HCI)
* Accessibility systems
* Smart home environments
* Interactive kiosks
* Contactless control interfaces

---

## Conclusion

This project demonstrates how Computer Vision and Machine Learning-based hand tracking can be used to create intuitive and contactless user interfaces. By combining OpenCV and MediaPipe, the system provides real-time brightness control through simple hand gestures, showcasing the potential of gesture-based interaction technologies.

---

## References

1. OpenCV Documentation
2. MediaPipe Documentation
3. Python Official Documentation
4. Screen Brightness Control Documentation
5. GeeksforGeeks – Brightness Control with Hand Detection Using OpenCV in Python
