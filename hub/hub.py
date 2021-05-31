# run this program to display image streams from multiple clients
import cv2
import imagezmq
from datetime import datetime
import imutils
import numpy as np
import argparse
import logging

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--rows", default=2, help="No. of rows created in resulting stream")
ap.add_argument("-c", "--cols", default=2, help="No. of columns created in resulting stream")
ap.add_argument("-d", "--dynamic", default=False, action="store_true", help="Enable dynamic resizing resulting video stream basing on clients count")
args = vars(ap.parse_args())

# number of clients in final stream change for parameters
ROWS = int(args["rows"]) 
COLS = int(args["cols"])
CLIENTS_NUMBER = ROWS * COLS

ACTIVITY_CHECK_PERIOD = 5
# how often will the activity be checked
ACTIVITY_CHECK_TIME = CLIENTS_NUMBER * ACTIVITY_CHECK_PERIOD

logging.basicConfig(format="[%(levelname)s][%(asctime)s][hub]: %(message)s", level=logging.INFO)
if not args["dynamic"]:
    logging.info("Resulting stream will use {} row(s) and {} column(s)".format(args["rows"], args["cols"]))
else:
    logging.info("Resulting stream will be resized dynamically")

# frames from all clients
frames = {}

# time when clients were last time active
last_active_time = {}
last_active_check = datetime.now()

# hub for connection with client
client = imagezmq.ImageHub()
# non-blocking server connection
server = imagezmq.ImageSender(connect_to = 'tcp://*:5566', REQ_REP = False)

logging.info("Hub started")
while True:
    # receive image from client
    client_id, frame = client.recv_image()
    client.send_reply(b'OK')

    if client_id not in last_active_time.keys():
        logging.info("New client with id {} connected".format(client_id))
    
    last_active_time[client_id] = datetime.now()

    clients_count = len(last_active_time.keys())

    # prepare received frame
    if clients_count != 1:
        frame = imutils.resize(frame, width=400)
    
    (h, w) = frame.shape[:2]

    # insert text about client name and current timestamp
    cv2.putText(frame, "{} {}".format(client_id, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))), (10, 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #insert text about client count
    client_number = str(list(last_active_time.keys()).index(client_id) + 1)
    cv2.putText(frame, client_number, (w - 20, h - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)

    # save to all frames
    frames[client_id] = frame

    # create montage from all frames
    if not args["dynamic"] and clients_count != 1:
        montages = imutils.build_montages(frames.values(), (w, h), (COLS, ROWS))
    elif args["dynamic"] and clients_count != 1:
        columns = 3 if clients_count >= 3 else 2
        remainer = 0
        if columns == 3 and clients_count % 3 != 0:
            remainer = 1
        elif columns == 2 and clients_count % 2 != 0:
            remainer = 1
        rows = clients_count // 3 if columns == 3 else clients_count // 2
        rows += remainer
        montages = imutils.build_montages(frames.values(), (w, h), (columns, rows))
    
    # send built montage
    if clients_count == 1:
        server.send_image(client_id, frame)
    else:
        for montage in montages:
            server.send_image(client_id, montage)

    if (datetime.now() - last_active_check).seconds > ACTIVITY_CHECK_TIME:
        logging.info("Activity check")
        for (client_id, ts) in list(last_active_time.items()):
            if (datetime.now() - ts).seconds > ACTIVITY_CHECK_TIME:
                logging.info("Lost connection with {}".format(client_id))
                last_active_time.pop(client_id)
                frames.pop(client_id) # remove frame from nonactive client
                
        last_active_check = datetime.now()