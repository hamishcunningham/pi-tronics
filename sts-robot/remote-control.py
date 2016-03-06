#!/usr/bin/env python

# sudo apt-get install python-picamera python-pip python-rpi.gpio
# sudo pip install pibrella

import threading
import pibrella
import time
import BaseHTTPServer
import mjpeg6
import signal

dovideo = False

class ControlHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def redirect(s, location):
        s.send_response(302)
        s.send_header('Location', location)
        s.end_headers()

    def do_GET(s):
#        s.wfile.write("test")
#        print s.path

        # video feed control (this forces a refresh of the page)
        global dovideo
        if s.path == "/video1":
            dovideo = True
            s.redirect("/")
            return
        if s.path == "/video0":
            dovideo = False
            s.redirect("/")
            return

        # interactive page elements
        if s.path != "/":

            # forward for a short period
            if s.path == "/forward":
                pibrella.output.on()
                time.sleep(0.5)
                pibrella.output.off()

            # turn for a short period
            elif s.path == "/left":
                pibrella.output.f.on()
                time.sleep(0.5)
                pibrella.output.f.off()
            elif s.path == "/right":
                pibrella.output.e.on()
                time.sleep(0.5)
                pibrella.output.e.off()

            # forward indefinetely
            elif s.path == "/forwardstart":
                pibrella.output.on()
            elif s.path == "/forwardstop":
                pibrella.output.off()

            # turn indefinetely
            elif s.path == "/leftstart":
                pibrella.output.f.on()
            elif s.path == "/rightstart":
                pibrella.output.e.on()
            elif s.path == "/leftstop":
                pibrella.output.f.off()
            elif s.path == "/rightstop":
                pibrella.output.e.off()
            s.send_response(200)
            s.end_headers()
            s.wfile.write("done");
            return

        s.send_response(200)
        s.end_headers()
        s.wfile.write("""
<html><head><title>A simple, open robot</title>
<meta name="viewport" content="width=device-width, initial-scale=0.8">
<style>
body { font-size: xx-large; } h1 { } h3 { }
p table { text-align: center; }
table.control a { color: black; border: 3px solid black; padding: 1em; text-decoration: none !important; }
table.control { padding: 3px; margin-bottom: 2.5em; font-size: xx-large; margin-left:auto; margin-right:auto; }
p.control a { color: black; border: 3px solid black; padding: 1em; text-decoration: none !important; }
p.control { padding: 3px; margin-bottom: 2.5em; text-align: center; }
p.control img { margin-left: 20px; }
</style>
</head><body>

<p><br/></p>

<p><table class="control">
<tr>
<td>NUDGE:</td>
<td><a href="/left" target="myframe">&lArr;</a></td>
<td><a href="/forward" target="myframe">&uArr;</a></td>
<td><a href="/right" target="myframe">&rArr;</a></td>
</tr>
<tr><td>&nbsp;<br/><br/></td></tr>
<tr>
<td>GO:</td>
<td><a href="/leftstart" target="myframe">&lArr;</a></td>
<td><a href="/forwardstart" target="myframe">&uArr;</a></td>
<td><a href="/rightstart" target="myframe">&rArr;</a></td>
</tr>
<tr><td>&nbsp;<br/><br/></td></tr>
<tr>
<td>STOP:</td>
<td><a href="/leftstop" target="myframe">&lArr;</a></td>
<td><a href="/forwardstop" target="myframe">&uArr;</a></td>
<td><a href="/rightstop" target="myframe">&rArr;</a></td>
</tr>
</table>

""")

        if dovideo == False:
            s.wfile.write('<p class="control">VIDEO: <a href="/video1">On</a></p>\n')
        else:
            myip = s.request.getsockname();
            s.wfile.write(
              '<p class="control">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="http://' +
              myip[0] + ':8080/t.mjpg"></p>\n'
            )
            s.wfile.write('<p class="control">VIDEO: <a href="/video0">Off</a></p>\n')

        s.wfile.write("""

<iframe src="/blank" name="myframe" style="display: none"></iframe>
</body></html>
        """)


class ServerThread(threading.Thread):
    def __init__(self, aserver):
        threading.Thread.__init__(self)
        self.aserver = aserver

    def run(self):
        self.aserver.serve_forever()

recorder=mjpeg6.VideoRecorder()
videohttpd=mjpeg6.ThreadedVideoServer(recorder, ("0.0.0.0", 8080), mjpeg6.VideoServerHandler)
videohttpdthread = ServerThread(videohttpd)

controlhttpd=BaseHTTPServer.HTTPServer(("0.0.0.0", 80), ControlHandler)
controlhttpdthread=ServerThread(controlhttpd)

print "Starting Video Capture..."
recorder.start()
print "Starting Video Server..."
videohttpdthread.start()
print "Starting Control Server..."
controlhttpdthread.start()

sleeping = 1

def quit_nicely():
    print "Stopping Video Capture..."
    recorder.running = False
    print "Stopping Video Server..."
    videohttpd.shutdown()
    print "Stopping Control Server..."
    controlhttpd.shutdown()

def signal_term_handler(signal, frame):
    print "SIGTERM recieved, shutting down..."
    global sleeping
    sleeping = 0
 
signal.signal(signal.SIGTERM, signal_term_handler)

try:
    print "Waiting for requests..."
    while sleeping:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit) as e:
    pass
quit_nicely()
