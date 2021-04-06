"""send_image.py -- send PiCamera jpg stream.

This program requires that the image receiving program be running first.
"""

import socket
import time
from imutils.video import VideoStream
import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://127.0.0.1:5555')

hostname = socket.gethostname()
stream = VideoStream(usePiCamera=False).start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:
    image = stream.read()
    sender.send_image(hostname, image)