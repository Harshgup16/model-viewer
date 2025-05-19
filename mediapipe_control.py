import eventlet
eventlet.monkey_patch()  # Important: Must be first!

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# MediaPipe Setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Webcam capture setup
cap = cv2.VideoCapture(0)

def process_hand_gestures():
    while True:
        success, frame = cap.read()
        if not success:
            print("Webcam frame not read successfully.")
            time.sleep(0.1)
            continue

        # Flip the image and convert color
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        hand_data = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append({'x': lm.x, 'y': lm.y, 'z': lm.z})
                hand_data.append(landmarks)

                # Optional: draw on frame
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            print("Emitting hand data:", hand_data)
            socketio.emit('hand_data', hand_data)
        else:
            print("No hand detected, emitting empty hand_data.")
            socketio.emit('hand_data', [])

        # Optional: show live feed
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    # Run camera processing in a background task
    socketio.start_background_task(process_hand_gestures)
    # Start Flask with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)