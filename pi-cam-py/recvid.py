# recvid.py

import picamera
import datetime

while(True):
    with picamera.PiCamera() as cam:
	cam.start_recording("video-" + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S") + ".h264")
        cam.wait_recording(60)
	cam.stop_recording()
