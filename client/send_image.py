"""send_image.py -- send PiCamera jpg stream.

This program requires that the image receiving program be running first.
"""

import sys

import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq

# use either of the formats below to specifiy address of display computer
sender = imagezmq.ImageSender(connect_to='tcp://127.0.0.1:5555')

name = socket.gethostname()  # send client name with each image
picam = VideoStream(usePiCamera=False).start()
time.sleep(2.0)  #allow camera to warm up
img_quality = 95
while True:
    image = picam.read()
    ret_code, jpg_buffer = cv2.imencode(
        ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), img_quality])
    sender.send_jpg(name, jpg_buffer)
