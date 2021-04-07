import socket
import time
from imutils.video import VideoStream
import imagezmq

# connection with hub
sender = imagezmq.ImageSender(connect_to='tcp://127.0.0.1:5555')
host_name = socket.gethostname()

print("[INFO] Client started!\nHostname:{}...".format(host_name))
stream = VideoStream().start()
time.sleep(2.0)  # allow camera sensor to warm up

print("[INFO] Streaming now...")
while True:
    frame = stream.read()
    sender.send_image(host_name, frame)