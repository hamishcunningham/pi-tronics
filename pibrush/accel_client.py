import socket
import XLoBorg
import time

# network stufff
server = "modelb"
port = 5005

# setup for the accelerometer
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

# make the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    message = '%+01.4f,%+01.4f,%+01.4f' \
            % XLoBorg.ReadAccelerometer()
    sock.sendto(message, (server, port))
    time.sleep(0.005)
