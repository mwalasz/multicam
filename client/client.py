"""send_image.py -- send PiCamera jpg stream.

This program requires that the image receiving program be running first.
"""

import socket
import time
from imutils.video import VideoStream
import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://127.0.0.1:5555')

hostname = socket.gethostname()
picam = VideoStream(usePiCamera=False).start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:
    image = picam.read()
    sender.send_image(hostname, image)