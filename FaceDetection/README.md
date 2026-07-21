# Real-Time Face and Eye Detection Using OpenCV

## Overview

Real-Time Face and Eye Detection is a Computer Vision project developed using Python and OpenCV. The application captures live video from a webcam and detects human faces and eyes in real time using Haar Cascade Classifiers.

Detected faces are highlighted with bounding boxes, while eyes within each detected face are identified and marked separately. The system also displays the total number of detected faces and the current Frames Per Second (FPS), providing performance monitoring during execution.

This project demonstrates fundamental concepts of image processing, object detection, and real-time video analysis, making it suitable for beginners exploring Computer Vision and OpenCV.

---

## Features

* Real-time face detection using a webcam
* Eye detection within detected faces
* Face count display
* FPS (Frames Per Second) monitoring
* Bounding boxes and labels for detected objects
* Lightweight and efficient implementation
* Easy to extend for advanced face recognition systems

---

## Technologies Used

* Python 3.x
* OpenCV
* Haar Cascade Classifiers
* NumPy

---

## How It Works

1. The webcam continuously captures video frames.
2. Each frame is converted to grayscale for efficient processing.
3. The Haar Cascade face detector scans the frame and identifies faces.
4. For each detected face, a Region of Interest (ROI) is created.
5. The eye detector analyzes the ROI and locates eyes.
6. Bounding boxes and labels are drawn around detected faces and eyes.
7. The system calculates and displays FPS and the number of faces detected in real time.

---

## Project Structure

```text
FaceDetection/
│
├── face_detection.py
├── README.md
├── requirements.txt
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/JayasreeAB/Image-Visualization-Projects.git
```

### Navigate to the Project Folder

```bash
cd FaceDetection
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

---

## Running the Project

```bash
python face_detection.py
```

---

## Controls

| Key | Action           |
| --- | ---------------- |
| Q   | Quit Application |

---

## Sample Output

The application displays:

* Webcam feed
* Face detection rectangles
* Eye detection rectangles
* Face count
* FPS value

Example:

```text
Faces: 1
FPS: 30
```

---


## Applications

* Face tracking systems
* Attendance monitoring systems
* Human-Computer Interaction
* Security and surveillance
* Camera-based automation
* Computer Vision learning projects

---

## Learning Outcomes

Through this project, the following concepts can be understood:

* Image processing fundamentals
* Grayscale image conversion
* Haar Cascade object detection
* Real-time video processing
* Region of Interest (ROI) analysis
* Performance measurement using FPS
* OpenCV-based application development

---

## Conclusion

This project demonstrates a practical implementation of real-time face and eye detection using OpenCV. By combining Haar Cascade classifiers with live webcam input, the system efficiently detects and tracks faces and eyes while providing useful performance metrics.

The project serves as an excellent introduction to Computer Vision and forms a foundation for more advanced AI-powered facial analysis applications.
