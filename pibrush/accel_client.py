import socket
import XLoBorg
import time

# network stufff
server = "192.168.1.64"
port = 5005

# setup for the accelerometer
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

# make the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
#    acceleration = 'X = %+01.4f G, Y = %+01.4f G, Z = %+01.4f G' % XLoBorg.ReadAccelerometer()
    acceleration = '%+01.4f,%+01.4f,%+01.4f' % XLoBorg.ReadAccelerometer()
#    compass = 'mX = %+06d, mY = %+06d, mZ = %+06d' % XLoBorg.ReadCompassRaw()
    compass = '%+06d,%+06d,%+06d' % XLoBorg.ReadCompassRaw()
    message = '%s, %s' %(acceleration, compass)
    sock.sendto(message, (server, port))
    time.sleep(0.005)
