#!/usr/bin/env python

import pibrella
import time
import BaseHTTPServer


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
#        s.wfile.write("test")
#        print s.path
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
            s.wfile.write('<html><head><meta http-equiv=\"refresh"\ content=\"2\"></head><body><p align=\"center\"><img src="/test.jpg" width=\"640\" height=\"480\"></p></body></html>')
            return

        # forward for a short period
        if s.path == "/forward":
            pibrella.output.on()
            time.sleep(0.5)
            pibrella.output.off()

        # turn for a short period
        if s.path == "/left":
            pibrella.output.f.on()
            time.sleep(0.5)
            pibrella.output.f.off()
        if s.path == "/right":
            pibrella.output.e.on()
            time.sleep(0.5)
            pibrella.output.e.off()

        # forward indefinetely
        if s.path == "/forwardstart":
            pibrella.output.on()
        if s.path == "/forwardstop":
            pibrella.output.off()

        # turn indefinetely
        if s.path == "/leftstart":
            pibrella.output.f.on()
        if s.path == "/rightstart":
            pibrella.output.e.on()
        if s.path == "/leftstop":
            pibrella.output.f.off()
        if s.path == "/rightstop":
            pibrella.output.e.off()

#        if s.path == "/":
        s.send_response(200)
        s.end_headers()
        s.wfile.write("<head><style>a { font-size: large; color: black; border: 3px solid black; padding: 20px; } p { padding: 3px }</style></head>")
        s.wfile.write("<body><h1 align=\"center\">A simple, open robot</h1><p><br/>")
#        s.wfile.write("<body style=\"font-size: 200%\">")
        s.wfile.write("<p align=\"center\"><a href=\"/forward\">forward</a> ")
        s.wfile.write("<a href=\"/left\">left</a> ")
        s.wfile.write("<a href=\"/right\">right</a></p>")
        s.wfile.write("<p align=\"center\">&nbsp;</p>")
        s.wfile.write("<p align=\"center\"><a href=\"/forwardstart\">forwardstart</a> ")
        s.wfile.write("<a href=\"/forwardstop\">forwardstop</a></p>")

        s.wfile.write("<p align=\"center\">&nbsp;</p>")
        s.wfile.write("<p align=\"center\"><a href=\"/leftstart\">leftstart</a> ")
        s.wfile.write("<a href=\"/leftstop\">leftstop</a></p>")

        s.wfile.write("<p align=\"center\">&nbsp;</p>")
        s.wfile.write("<p align=\"center\"><a href=\"/rightstart\">rightstart</a> ")
        s.wfile.write("<a href=\"/rightstop\">rightstop</a></p>")

#        s.wfile.write("<p><br/><p align=\"center\"><iframe src=\"/test.html\" width=\"680\" height=\"520\"></iframe></p>")
        s.wfile.write("</body>")


server_class=BaseHTTPServer.HTTPServer
httpd=server_class(("0.0.0.0", 80), MyHandler)
httpd.serve_forever()

