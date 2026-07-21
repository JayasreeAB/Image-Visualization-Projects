import base64
import time
import cv2
import numpy as np
from math import hypot
from flask import Flask, render_template, request, jsonify, Response

# Optional import for screen brightness control
try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except Exception as e:
    SBC_AVAILABLE = False
    print("screen_brightness_control not available or failed to load:", e)

# Mediapipe for Hand Tracking
import mediapipe as mp

print("MediaPipe module:", mp)
print("MediaPipe file:", getattr(mp, "__file__", "No file"))
print("MediaPipe attributes:", dir(mp)[:20])

app = Flask(__name__)

# Initialize Haar Cascades for Face & Eye Detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2
)
mp_draw = mp.solutions.drawing_utils

# Store server state
current_system_brightness = 50

def safe_set_brightness(level):
    """Safely update system brightness if SBC is available."""
    global current_system_brightness
    current_system_brightness = int(level)
    if SBC_AVAILABLE:
        try:
            sbc.set_brightness(current_system_brightness)
            return True
        except Exception as err:
            print(f"Error setting system brightness: {err}")
            return False
    return False

def safe_get_brightness():
    """Safely get system brightness if SBC is available."""
    if SBC_AVAILABLE:
        try:
            b = sbc.get_brightness()
            if isinstance(b, list) and len(b) > 0:
                return b[0]
            elif isinstance(b, int):
                return b
        except Exception:
            pass
    return current_system_brightness

def process_frame(frame, mode='dual', min_neighbors=5, scale_factor=1.1, min_conf=0.7):
    """
    Process OpenCV frame according to requested mode: 'face', 'hand', or 'dual'.
    Returns processed frame, face count, brightness level, gesture distance, and FPS.
    """
    h, w, _ = frame.shape
    face_count = 0
    b_level = None
    gesture_distance = None

    # Horizontal flip for intuitive webcam mirror mode
    frame = cv2.flip(frame, 1)

    # --- 1. FACE DETECTION PIPELINE ---
    if mode in ['face', 'dual']:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=float(scale_factor),
            minNeighbors=int(min_neighbors),
            minSize=(30, 30)
        )
        face_count = len(faces)

        for (x, y, fw, fh) in faces:
            # Face Bounding Box
            cv2.rectangle(frame, (x, y), (x + fw, y + fh), (255, 100, 0), 2)
            
            # Label background box
            cv2.rectangle(frame, (x, y - 25), (x + 75, y), (255, 100, 0), -1)
            cv2.putText(
                frame, "FACE", (x + 5, y - 7),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
            )

            # Eye Detection within Face ROI
            roi_gray = gray[y:y+fh, x:x+fw]
            roi_color = frame[y:y+fh, x:x+fw]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 180), 1)

        # Draw Face Count Badge on Top-Left
        badge_text = f"Faces Detected: {face_count}"
        cv2.putText(frame, badge_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # --- 2. HAND GESTURE BRIGHTNESS PIPELINE ---
    if mode in ['hand', 'dual']:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        process_res = hands.process(frame_rgb)

        landmark_list = []
        if process_res.multi_hand_landmarks:
            for hand_lm in process_res.multi_hand_landmarks:
                for idx, lm in enumerate(hand_lm.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmark_list.append([idx, cx, cy])
                
                # Draw hand skeleton connections
                mp_draw.draw_landmarks(
                    frame, hand_lm, mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 215, 255), thickness=2, circle_radius=3),
                    mp_draw.DrawingSpec(color=(255, 0, 128), thickness=2)
                )

        if len(landmark_list) >= 9:
            # Thumb tip = ID 4, Index tip = ID 8
            x1, y1 = landmark_list[4][1], landmark_list[4][2]
            x2, y2 = landmark_list[8][1], landmark_list[8][2]

            # Highlights on tips
            cv2.circle(frame, (x1, y1), 9, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 9, (0, 255, 0), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # Midpoint & Distance
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            gesture_distance = int(hypot(x2 - x1, y2 - y1))

            # Interpolate distance (15 - 200 px) to brightness percentage (0 - 100 %)
            calculated_b = float(np.interp(gesture_distance, [20, 200], [0, 100]))
            b_level = int(calculated_b)

            # Update system brightness
            safe_set_brightness(b_level)

            # Draw visual indicator at midpoint
            cv2.circle(frame, (mid_x, mid_y), 7, (255, 255, 255), cv2.FILLED)
            cv2.putText(
                frame, f"{b_level}%", (mid_x + 10, mid_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
            )

        # Draw Brightness Bar on Right Edge
        b_val = b_level if b_level is not None else safe_get_brightness()
        bar_height = int(np.interp(b_val, [0, 100], [350, 100]))
        cv2.rectangle(frame, (w - 40, 100), (w - 15, 350), (60, 60, 60), 2)
        cv2.rectangle(frame, (w - 40, bar_height), (w - 15, 350), (0, 255, 128), -1)
        cv2.putText(
            frame, f"{b_val}%", (w - 55, 380),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 128), 2
        )

    return frame, face_count, b_level, gesture_distance

@app.route('/')
def index():
    """Render main application dashboard."""
    initial_brightness = safe_get_brightness()
    return render_template('index.html', initial_brightness=initial_brightness, sbc_available=SBC_AVAILABLE)

@app.route('/api/process_frame', methods=['POST'])
def api_process_frame():
    """
    API Endpoint: Receives client webcam base64 frame data, runs computer vision processing,
    and returns annotated frame base64 + metadata JSON.
    """
    start_time = time.time()
    try:
        data = request.get_json(force=True)
        image_data = data.get('image', '')
        mode = data.get('mode', 'dual')
        min_neighbors = data.get('min_neighbors', 5)
        scale_factor = data.get('scale_factor', 1.1)

        if ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'status': 'error', 'message': 'Failed to decode image frame'}), 400

        processed_frame, face_count, b_level, gesture_dist = process_frame(
            frame, mode=mode, min_neighbors=min_neighbors, scale_factor=scale_factor
        )

        # Encode processed frame back to base64 JPEG
        _, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        encoded_image = base64.b64encode(buffer).decode('utf-8')

        elapsed = time.time() - start_time
        fps = round(1.0 / elapsed, 1) if elapsed > 0 else 30.0

        return jsonify({
            'status': 'success',
            'image': f'data:image/jpeg;base64,{encoded_image}',
            'face_count': face_count,
            'brightness': b_level if b_level is not None else safe_get_brightness(),
            'distance': gesture_dist if gesture_dist is not None else 0,
            'fps': fps
        })

    except Exception as e:
        print("Error processing frame:", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/set_brightness', methods=['POST'])
def api_set_brightness():
    """API Endpoint to manually adjust screen brightness from UI slider."""
    try:
        data = request.get_json(force=True)
        level = int(data.get('brightness', 50))
        success = safe_set_brightness(level)
        return jsonify({'status': 'success', 'brightness': level, 'system_updated': success})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def generate_local_stream():
    """Generator for local OpenCV camera stream (Server Direct Mode)."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    prev_t = time.time()
    while True:
        success, frame = cap.read()
        if not success:
            break

        processed_frame, _, _, _ = process_frame(frame, mode='dual')
        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()

@app.route('/api/video_feed')
def video_feed():
    """Streaming route for local direct webcam access."""
    return Response(generate_local_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Starting Vision Hub Web Application on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
