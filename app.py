from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

@app.route('/')
def index():
    return render_template('index.html')

# Example: emit dummy hand data for testing
import time
import threading

def send_hand_data():
    import random
    while True:
        # Simulate hand landmark data
        data = [[[random.random() for _ in range(3)] for _ in range(21)]]
        socketio.emit('hand_data', data)
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=send_hand_data, daemon=True).start()
    socketio.run(app, debug=True)