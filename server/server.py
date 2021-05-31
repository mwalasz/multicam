import cv2
from flask import Flask, Response
import imagezmq
import argparse
import logging

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", default=4000, help="Port on which server starts")
args = vars(ap.parse_args())

logging.basicConfig(format="[%(levelname)s][%(asctime)s][server]: %(message)s", level=logging.INFO)
logging.info("Trying to start server on port {}".format(args["port"]))

def sendImagesToWeb():
    # When we have incoming request, create a receiver and subscribe to a publisher
    while True:
        receiver = imagezmq.ImageHub(open_port='tcp://localhost:5566', REQ_REP = False)
        # Pull an image from the queue
        camName, frame = receiver.recv_image()
        # Using OpenCV library create a JPEG image from the frame we have received
        jpg = cv2.imencode('.jpg', frame)[1]
        # Convert this JPEG image into a binary string that we can send to the browser via HTTP
        yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+jpg.tostring()+b'\r\n'

app = Flask(__name__)

@app.route('/')
def index():
    return Response(sendImagesToWeb(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=args["port"], debug=True)