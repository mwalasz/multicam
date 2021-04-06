""" receive and display jpg stream.

1. Run this program in its own terminal:
python receive_image.py

2. Run the jpg sending program on the other terminal:
python send_image.py

To end the programs, press Ctrl-C in the terminal window of the client first.
"""
import sys

import numpy as np
import cv2
import imagezmq

image_hub = imagezmq.ImageHub()
while True:
    client_name, jpg_buffer = image_hub.recv_jpg()
    image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)
    cv2.imshow(client_name, image)  # one window per client
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')
