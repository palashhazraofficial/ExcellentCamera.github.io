from flask import Flask, render_template, Response, request
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)
current_mode = "normal"

def generate_frames():
    global current_mode
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if current_mode == "grey":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif current_mode == "heatmap":
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.applyColorMap(grey, cv2.COLORMAP_JET)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_mode/<mode>')
def set_mode(mode):
    global current_mode
    current_mode = mode
    return f"Mode changed to {mode}"

camera_index = 0

@app.route('/switch_camera')
def switch_camera():
    global camera, camera_index
    camera_index = 1 if camera_index == 0 else 0  
    camera.release()
    camera = cv2.VideoCapture(camera_index)
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
