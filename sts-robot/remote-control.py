#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import BaseHTTPServer

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
#GPIO.output(22, True)
#time.sleep(1)
#GPIO.output(22, False)


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
#		s.wfile.write("test")
#		print s.path
		if s.path == "/test.jpg":
			f = open('test.jpg', 'rb')
			s.send_response(200)
			s.send_header("Content-type", "image/jpg")
			s.end_headers()
			s.wfile.write(f.read())
			return
		if s.path == "/test.html":
			s.send_response(200)
			s.end_headers()
			s.wfile.write('<html><head><meta http-equiv=\"refresh"\ content=\"1\"></head><body><img src="/test.jpg" width=\"640\" height=\"480\"></body></html>')
			return

		if s.path == "/forward":
			GPIO.output(22, True)
			GPIO.output(23, True)
			time.sleep(0.5)
			GPIO.output(22, False)
			GPIO.output(23, False)
		if s.path == "/forwardstart":
			GPIO.output(22, True)
			GPIO.output(23, True)
		if s.path == "/forwardstop":
			GPIO.output(22, False)
			GPIO.output(23, False)
		if s.path == "/left":
			GPIO.output(23, True)
			time.sleep(0.5)
			GPIO.output(23, False)
		if s.path == "/right":
			GPIO.output(22, True)
			time.sleep(0.5)
			GPIO.output(22, False)

		if s.path == "/leftstart":
			GPIO.output(23, True)
		if s.path == "/rightstart":
			GPIO.output(22, True)
		if s.path == "/leftstop":
			GPIO.output(23, False)
		if s.path == "/rightstop":
			GPIO.output(22, False)

#		if s.path == "/":
		s.send_response(200)
		s.end_headers()
		s.wfile.write("<head><style>a { font-size: large; color: black; border: 3px solid black; padding: 20px; } p { padding: 3px }</style></head>")
		s.wfile.write("<body>")
#		s.wfile.write("<body style=\"font-size: 200%\">")
		s.wfile.write("<p><a href=\"/forward\">forward</a> ")
		s.wfile.write("<a href=\"/left\">left</a> ")
		s.wfile.write("<a href=\"/right\">right</a></p>")
		s.wfile.write("<p>&nbsp;</p>")
		s.wfile.write("<p><a href=\"/forwardstart\">forwardstart</a> ")
		s.wfile.write("<a href=\"/forwardstop\">forwardstop</a></p>")

		s.wfile.write("<p>&nbsp;</p>")
		s.wfile.write("<p><a href=\"/leftstart\">leftstart</a> ")
		s.wfile.write("<a href=\"/leftstop\">leftstop</a></p>")

		s.wfile.write("<p>&nbsp;</p>")
		s.wfile.write("<p><a href=\"/rightstart\">rightstart</a>")
		s.wfile.write("<a href=\"/rightstop\">rightstop</a></p>")

		s.wfile.write("<iframe src=\"/test.html\" width=\"680\" height=\"520\"></iframe>")
		s.wfile.write("</body>")


server_class=BaseHTTPServer.HTTPServer
httpd=server_class(("0.0.0.0", 8080), MyHandler)
httpd.serve_forever()

