# Image Visualization Projects & Vision Hub Web AI

A collection of Computer Vision and Image Processing projects developed using Python, OpenCV, MediaPipe, Flask, and JavaScript.

This repository features an interactive **Vision Hub Web Application** that combines both computer vision models (Face Counting & Eye Tracking + Hand Gesture Brightness Control) into a single web dashboard.

---

## 🌟 Vision Hub Web Application

Access your webcam directly from the web browser, view real-time processed video streams, toggle between detection modes, adjust sensitivity parameters, and control screen brightness!

### Key Features:
* 👁️ **Face Counter & Eye Tracker**: Real-time multi-face bounding boxes, eye highlights, face counter badge, and FPS monitoring.
* 🖐️ **Hand Gesture Brightness Control**: Track hand landmarks, pinch thumb and index finger to dynamically adjust screen & webpage brightness.
* 🔀 **Dual Vision Mode**: Run face detection and hand tracking simultaneously on live video streams.
* 💻 **Dual Camera Engine**:
  * **Client Browser Webcam** (`navigator.mediaDevices.getUserMedia`) for cloud web deployments.
  * **Server Direct Camera Mode** (OpenCV `VideoCapture`) for local execution.
* 🎛️ **Interactive Controls**: Manual brightness slider, face detection `minNeighbors` and `scaleFactor` adjustment sliders, real-time snapshot export.

---

## 🚀 How to Run Locally

### Option 1: Double-Click Batch Launcher (Windows)
Double-click `run_app.bat` in the project root. It will activate the `venv` and open `http://127.0.0.1:5000` automatically in your browser!

### Option 2: Python Command Line
```bash
# 1. Activate Virtual Environment
.\venv\Scripts\activate

# 2. Run Application
python run_app.py
```
Open `http://127.0.0.1:5000` in your web browser.

---

## ☁️ Deployment Instructions

### Deploy to Render / Railway / Heroku
This project is deployment-ready with included `Procfile`, `render.yaml`, and `requirements.txt`.

1. Push code to GitHub.
2. Create a **Web Service** on Render or Railway connected to your repository.
3. Build Command:
   `pip install -r requirements.txt`
4. Start Command:
   `gunicorn app:app`
5. Visit your public web app URL! Because the app uses browser webcam access (`getUserMedia`), it works on cloud servers without physical camera hardware.

### Deploy with Docker
```bash
docker build -t vision-hub .
docker run -p 5000:5000 vision-hub
```

---

## 📁 Repository Structure

```text
OpenCV/
├── app.py                   # Flask server & OpenCV/MediaPipe pipeline
├── run_app.py               # Launcher script with auto browser opening
├── run_app.bat              # One-click Windows batch launcher
├── requirements.txt         # Consolidated Python dependencies
├── Procfile                 # Deployment file for Heroku/Render
├── render.yaml              # Render blueprint config
├── Dockerfile               # Docker build specification
├── templates/
│   └── index.html           # Glassmorphic Web Dashboard UI
├── static/
│   ├── css/style.css        # Modern dark theme styles & animations
│   └── js/app.js            # Client camera handler & stream processing
├── FaceDetection/
│   └── face_detection.py    # Original standalone script
├── HandBrightnessControl/
│   └── brightness_control.py # Original standalone script
└── venv/                    # Virtual environment
```

---

## 🛠️ Technologies Used

* **Core & Vision**: Python 3.11, OpenCV, MediaPipe, NumPy, Screen-Brightness-Control
* **Backend Web Framework**: Flask, Gunicorn
* **Frontend**: HTML5 Canvas, Vanilla CSS (Glassmorphism, Dark Mode), JavaScript (Webcam API, Fetch, DOM)

---

## Author

**Jayasree A B**  
Computer Vision and Image Processing Web Projects.
