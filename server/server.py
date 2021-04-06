# run http server

import cv2
import imagezmq
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

def sendImagesToWeb():
    # When we have incoming request, create a receiver and subscribe to a publisher
    receiver = imagezmq.ImageHub(open_port='tcp://localhost:5566', REQ_REP = False)
    while True:
        # Pull an image from the queue
        camName, frame = receiver.recv_image()
        # Using OpenCV library create a JPEG image from the frame we have received
        jpg = cv2.imencode('.jpg', frame)[1]
        # Convert this JPEG image into a binary string that we can send to the browser via HTTP
        yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+jpg.tostring()+b'\r\n'

@Request.application
def application(request):
    return Response(sendImagesToWeb(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    run_simple('127.0.0.1', 4000, application)