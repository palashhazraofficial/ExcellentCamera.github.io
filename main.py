from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)
current_mode = "normal"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_mode/<mode>')
def set_mode(mode):
    global current_mode
    current_mode = mode
    return jsonify({"status": "ok", "mode": mode})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global current_mode
    data = request.json['image']
    header, encoded = data.split(",", 1)
    nparr = np.frombuffer(base64.b64decode(encoded), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if current_mode == "grey":
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    elif current_mode == "heatmap":
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.applyColorMap(grey, cv2.COLORMAP_JET)

    _, buffer = cv2.imencode('.jpg', frame)
    processed_base64 = base64.b64encode(buffer).decode('utf-8')
    return jsonify({"image": f"data:image/jpeg;base64,{processed_base64}"})

if __name__ == "__main__":
    app.run()
