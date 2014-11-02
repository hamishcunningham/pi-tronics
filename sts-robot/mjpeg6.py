#!/usr/bin/env python

import time
import BaseHTTPServer
import threading
from SocketServer import ThreadingMixIn
import io
import picamera

FRAMERATE = 1.0/10

class VideoRecorder(threading.Thread):

	def run(self):
		self.running = False
		self.camera = picamera.PiCamera()
		self.camera.stop_preview()
		self.camera.resolution = (320, 240)
		self.camera.vflip = True
		self.camera.hflip = True
		self.stream = io.BytesIO()
		self.running = True
		now = time.time()

		for foo in self.camera.capture_continuous(self.stream, use_video_port=True,format='jpeg',quality=100,thumbnail=None,bayer=False,burst=False):
			self.stream.seek(0)
			self.frameLocked = True
			self.frame = self.stream.read()
			self.frameLocked = False
			self.stream.seek(0)
			wait = time.time() - now
			while wait > FRAMERATE:
				wait -= FRAMERATE
			time.sleep(FRAMERATE - wait)
			if self.running == False:
				break
			now = time.time()
		self.camera.close()

class VideoServer(BaseHTTPServer.HTTPServer):
	def __init__(self, recorder, server_address, RequestHandlerClass):
		self.recorder = recorder
		BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)

class ThreadedVideoServer(ThreadingMixIn, VideoServer):
    pass

class VideoServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)

		if s.path == ('/t.mjpg'):
			s.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			s.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
			s.send_header('Connection', 'close')
			s.send_header('Pragma', 'no-cache')
			s.end_headers()

			while not s.wfile.closed and s.server.recorder.running:
				while s.server.recorder.frameLocked:
					time.sleep(FRAMERATE/10.0)
				s.send_header('Content-type','image/jpeg')
				s.send_header('Content-length',str(len(s.server.recorder.frame)))
				s.end_headers()
				s.wfile.write(s.server.recorder.frame)
				s.wfile.write("--jpgboundary")
				s.wfile.flush()
				time.sleep(FRAMERATE)
		else:
			s.end_headers()
			s.wfile.write('<body><img src="t.mjpg" width="480" height="360"></body>')

#r=VideoRecorder()
#httpd=ThreadedVideoServer(r, ("0.0.0.0", 8080), VideoServerHandler)
#try:
#	r.start()
#	httpd.serve_forever()
#except (KeyboardInterrupt, SystemExit) as e:
#	r.running = False
