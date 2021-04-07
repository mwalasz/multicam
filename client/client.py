import socket
import time
from imutils.video import VideoStream
import imagezmq

# connection with hub
sender = imagezmq.ImageSender(connect_to='tcp://127.0.0.1:5555')

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_id = "[{}/{}]".format(host_name, host_ip)
print("[INFO] Client started! Name: {}, IP: {}".format(host_name, host_ip))

stream = VideoStream().start()
time.sleep(2.0)  # allow camera sensor to warm up

print("[INFO] Streaming now...")
while True:
    frame = stream.read()
    sender.send_image(host_id, frame)