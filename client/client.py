import socket
import time
import imagezmq
import argparse
import logging
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--serverip", default="127.0.0.1", help="ip address of streaming server")
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
ap.add_argument("-n", "--name", default="{}/{}".format(host_name, host_ip), help="Name of client which will be printed on streamed video, default = [{hostname}/{IP}]")
args = vars(ap.parse_args())

# connection with hub
sender = imagezmq.ImageSender(connect_to='tcp://{}:5555'.format(args["serverip"]))
logging.basicConfig(format="[%(levelname)s][%(asctime)s][{}]: %(message)s".format(args["name"]), level=logging.INFO)

logging.info("Client started! Name: {}, IP: {}".format(args["name"], host_ip))

try:
    stream = cv2.VideoCapture(0)
except:
    logging.error("Failed to open camera - exiting")
    exit()

logging.info("Warming camera sensor")
time.sleep(2.0)  # allow camera sensor to warm up

logging.info("Starting stream...")
if stream.isOpened():
    logging.info("Successfully started stream")
else:
    logging.error("Failed to start stream - exiting")
    exit(-1)
video_watermark = "[{}]".format(args["name"])
while True:
    captured, frame = stream.read()
    if not captured:
        logging.error("Failed to capture current frame")
    else:
        sender.send_image(video_watermark, frame)
        