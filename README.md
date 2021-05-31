# Multicam - simple application for CCTV monitoring system ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/mwalasz/multicam) ![GitHub top language](https://img.shields.io/github/languages/top/mwalasz/multicam) ![Github All Contributors](https://img.shields.io/github/all-contributors/mwalasz/multicam) ![GitHub last commit](https://img.shields.io/github/last-commit/mwalasz/multicam)

Multicam is a simple Python application consisting of HTTP server, hub and client. Its goal is to send frames captured from webcamera on device running client script to hub,
which modifies received frames adding details about client's name, current timestamp and client's ordinal number starting from 1.
Server constantly pops made by hub frames and send them through HTTP to be available for watch in web browser or e.g. VLC.

### Prerequisites

- Python 3.8 installed on your system,
- required dependencies installed - to install them, run `pip install -r requirements.txt` command in project directory

### Usage:

- server:

```
python3 server/server.py -h
usage: server.py [-h] [-p PORT]

optional arguments:
 -h, --help            show this help message and exit
 -p PORT, --port PORT  Port on which server starts

```

- hub:

```
python3 hub/hub.py -h
usage: hub.py [-h] [-r ROWS] [-c COLS] [-d]

optional arguments:
 -h, --help            show this help message and exit
 -r ROWS, --rows ROWS  No. of rows created in resulting stream, default = 2
 -c COLS, --cols COLS  No. of columns created in resulting stream, default = 2
 -d, --dynamic         Enable dynamic resizing resulting video stream basing on clients count
```

- client:

```
python3 client/client.py -h
usage: client.py [-h] [-ip SERVERIP] [-n NAME]

optional arguments:
 -h, --help            show this help message and exit
 -ip SERVERIP, --serverip SERVERIP
                       ip address of streaming server
 -n NAME, --name NAME  Name of client which will be printed on streamed video, default = [{hostname}/{IP}]
```

## Screenshots

Example montage made by combining frames from 6 clients (with covered up webcameras :detective:):

![example_montage](./assets/example_montage.png)

### Steps to run:

1. `python .\server\server.py` to start http server
2. `python .\hub\hub.py` to start hub which intermediates between client and server
3. `python .\client\client.py` to start client which captures image from camera
4. Open stream: http://localhost:4000 in your browser or e.g. using VLC program

### Tech Stack:

- Python 3.8
- [ImageZMQ 1.1.1](https://github.com/jeffbass/imagezmq)
- [imutils 0.5.4](https://github.com/jrosebr1/imutils)
- [OpenCV 4.5.1.48](https://github.com/opencv/opencv)
- [Flask 1.1.2](https://github.com/pallets/flask)
