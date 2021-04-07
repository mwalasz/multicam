# run this program to display image streams from multiple clients
import cv2
import imagezmq
from datetime import datetime
import imutils
import numpy as np

# number of clients in final stream change for parameters
ROWS = 2
COLS = 2
CLIENTS_NUMBER = ROWS * COLS

ACTIVITY_CHECK_PERIOD = 5
# how often will the activity be checked
ACTIVITY_CHECK_TIME = CLIENTS_NUMBER * ACTIVITY_CHECK_PERIOD

def processImage(image):
    # somehow process image
    pass

# frames from all clients
frames = {}

# time when clients were last time active
last_active_time = {}
last_active_check = datetime.now()

# hub for connection with client
client = imagezmq.ImageHub()
# non-blocking server connection
server = imagezmq.ImageSender(connect_to = 'tcp://*:5566', REQ_REP = False)

print("[INFO] Hub started!")
while True:
    # receive image from client
    client_id, frame = client.recv_image()
    client.send_reply(b'OK')

    if client_id not in last_active_time.keys():
        print("[INFO] Receiving data from {}...".format(client_id))
    
    last_active_time[client_id] = datetime.now()

    # prepare received frame
    frame = imutils.resize(frame, width=400)
    (h, w) = frame.shape[:2]

    # insert text about client name
    cv2.putText(frame, client_id, (10, 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #insert text about client count
    client_number = str(list(last_active_time.keys()).index(client_id) + 1)
    cv2.putText(frame, client_number, (w - 20, h - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)

    # save to all frames
    frames[client_id] = frame

    # create montage from all frames
    montages = imutils.build_montages(frames.values(), (w, h), (ROWS, COLS))
    
    # send built montage
    for montage in montages:
        server.send_image(client_id, montage)

    if (datetime.now() - last_active_check).seconds > ACTIVITY_CHECK_TIME:
        print("[INFO] Activity check.")
        for (client_id, ts) in list(last_active_time.items()):
            if (datetime.now() - ts).seconds > ACTIVITY_CHECK_TIME:
                print("[INFO] lost connection to {}".format(client_id))
                last_active_time.pop(client_id)
                frames.pop(client_id) # remove frame from nonactive client
                
        last_active_check = datetime.now()