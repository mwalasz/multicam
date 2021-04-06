# run this program to display image streams from multiple clients
import cv2
import imagezmq

def processImage(image):
    # somehow process image
    pass

image_hub = imagezmq.ImageHub()

# non-blocking mode
stream_monitor = imagezmq.ImageSender(connect_to = 'tcp://*:5566', REQ_REP = False)

while True:
    client_name, image = image_hub.recv_image()
    image_hub.send_reply(b'OK')
    processImage(image)
    stream_monitor.send_image(client_name, image)