# run this program to display image streams from multiple clients
import cv2
import imagezmq
from datetime import datetime
import imutils
import numpy as np

# number of clients in final stream change for parameters
ROWS = 2
COLS = 2

def processImage(image):
    # somehow process image
    pass

# frames from all clients
frames = {}

# clients
last_active_client = {}
last_active = datetime.now()

# hub for connection with client
client = imagezmq.ImageHub()
# non-blocking server connection
server = imagezmq.ImageSender(connect_to = 'tcp://*:5566', REQ_REP = False)

print("[INFO] Hub started!")
while True:
    # receive image from client
    client_name, frame = client.recv_image()
    client.send_reply(b'OK')

    if client_name not in last_active_client.keys():
        print("[INFO] Receiving data from {}...".format(client_name))
    
    last_active_client[client_name] = datetime.now()

    # prepare received frame
    frame = imutils.resize(frame, width=400)
    (h, w) = frame.shape[:2]

    # save to all frames
    frames[client_name] = frame

    # create montage from all frames
    montages = imutils.build_montages(frames.values(), (w, h), (ROWS, COLS))
    
    # send built montage
    for montage in montages:
        server.send_image(client_name, montage)