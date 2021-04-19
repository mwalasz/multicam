import socket
import time
from imutils.video import VideoStream
import imagezmq
import argparse
import logging

ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--serverip", default="127.0.0.1", help="ip address of streaming server")
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
ap.add_argument("-n", "--name", default="{}/{}".format(host_name, host_ip), help="Name of client which will be printed on streamed video")
args = vars(ap.parse_args())

# connection with hub
sender = imagezmq.ImageSender(connect_to='tcp://{}:5555'.format(args["serverip"]))
logging.basicConfig(format="[%(levelname)s][%(asctime)s][{}]: %(message)s".format(args["name"]), level=logging.INFO)

logging.info("Client started! Name: {}, IP: {}".format(args["name"], host_ip))

stream = VideoStream().start()
logging.info("Warming camera sensor")
time.sleep(2.0)  # allow camera sensor to warm up

logging.info("Starting stream...")
video_watermark = "[{}]".format(args["name"])
while True:
    frame = stream.read()
    sender.send_image(video_watermark, frame)