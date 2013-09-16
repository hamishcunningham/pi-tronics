import socket
import select
import pygame
import time
import numpy
import math
import datetime

port = 5005

# setup networking
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", port))
sock.setblocking(0)

# setup display
pygame.init()
screen = pygame.display.set_mode((640, 400))
screen.fill((255, 255, 255))
myfont = pygame.font.SysFont("sans", 10)

# accelerometer storage for moving average
AL = 80 # length of moving average array
MAL = 15 # length of moving average
AXa = numpy.zeros((1, AL))
AYa = numpy.zeros((1, AL))
AZa = numpy.zeros((1, AL))

# store gravity when fast is detected..
GX = 0
GY = 0
GZ = 1

# polar gravity
PGR = 0
PGA = -math.pi
PGB = 0

# compass storage for moving average
CXa = numpy.zeros((1, AL))
CYa = numpy.zeros((1, AL))
CZa = numpy.zeros((1, AL))

# accelerometer values
AX = 0
AY = 0
AZ = 0

# compass values
CX = 0
CY = 0
CZ = 0

# headings
HXY = 0
HXZ = 0
HYZ = 0

# compass calibration
MACX = -3000
MICX = 3000
MACY = -3000
MICY = 3000
MACZ = -3000
MICZ = 3000

# =========
# functions
# =========

def text(X, Y, TEXT):
    label = myfont.render(TEXT, 1, (0, 0, 0))
    screen.blit(label, (X, Y))

def bartext(X, VAL, SCALE):
    VAL = round(VAL * 1000) / 1000
    if VAL > 0:
        aoff = 0
    else:
        aoff = -12
    text(X, 200 + VAL / SCALE * 200 + aoff, str(VAL))

def movingaverage(ARRAY, VALUE):
    ARRAY = numpy.append(ARRAY, [VALUE])
    ARRAY = numpy.delete(ARRAY, 0)
    l = numpy.shape(ARRAY)
    l = l[0]
    sub = ARRAY[l-MAL:l]
    return (numpy.sum(sub) / MAL, ARRAY)

def gravity(ARRAY):
    sub = ARRAY[0:MAL]
    return numpy.sum(sub) / MAL

# http://www.processing.org/discourse/beta/num_1236393966.html
def polar(X, Y, Z):
    x = numpy.linalg.norm([X, Y, Z])
    if (x > 0):
        y = -math.atan2(Z, X)
        z = math.asin(Y / x)
    else:
        y = 0
        z = 0
    return (x, y, z)

# http://electron9.phys.utk.edu/vectors/3dcoordinates.htm
def cartesian(X, A, B):
    x = X * math.sin(B) * math.cos(A)
    y = X * math.sin(B) * math.sin(A)
    z = X * math.cos(B)
    return (x, y, z)

def heading(X, Y):
    # compass heading (2D planar)
    # http://aeroquad.com/showthread.php?88-3-Axis-Magnetometer
    h = 0
    if X < 0:
        h = math.pi - math.atan(Y/X)
    elif X > 0 and Y < 0: 
        h = -math.atan(Y/X);
    elif X > 0 and Y > 0:
        h = 2 * math.pi - math.atan(Y/X);
    return h


# screen gravity
(PSGR, PSGA, PSGB) = polar(0, 0, 1)

# ============
# main program
# ============

fast = 0
running = 1
while running:
    # do networking
    result = select.select([sock], [], [], 0)
    if len(result[0]) > 0:
        # read in data
        data = result[0][0].recvfrom(1024)
#        message = data[0]
#        print "received message:", message
        a = data[0].split(",")
        AX = float(a[0])
        AY = float(a[1])
        AZ = float(a[2])
        CX = float(a[3]) * 0.1
        CY = float(a[4]) * 0.1
        CZ = float(a[5]) * 0.1

        # moving averages for acceleration
        (AX, AXa) = movingaverage(AXa, AX)
        (AY, AYa) = movingaverage(AYa, AY)
        (AZ, AZa) = movingaverage(AZa, AZ)

        # round gravity?
#        AX = round(AX * 10) / 10
#        AY = round(AY * 10) / 10
#        AZ = round(AZ * 10) / 10

        # moving averages for compass
        (CX, CXa) = movingaverage(CXa, CX)
        (CY, CYa) = movingaverage(CYa, CY)
        (CZ, CZa) = movingaverage(CZa, CZ)

        # compass calibration
        if CX > MACX:
            MACX = CX
        if CX < MICX:
            MICX = CX
        if CY > MACY:
            MACY = CY
        if CY < MICY:
            MICY = CY
        if CZ > MACZ:
            MACZ = CZ
        if CZ < MICZ:
            MICZ = CZ

        # https://www.sparkfun.com/products/10619#comment-4f07fe86ce395f5a76000000
        CX = CX - (MACX + MICX) / 2
        CY = CY - (MACY + MICY) / 2
        CZ = CZ - (MACZ + MICZ) / 2

        # headings
        HXY = heading(CX, CY)
#        HXZ = heading(CX, CZ)
#        HYZ = heading(CY, CZ)

    # check for a quit (or other events at some point I suppose)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    # =======
    # drawing
    # =======

    # reset to white
    screen.fill((255, 255, 255))

    # accelerometer bars
    pygame.draw.rect(screen, (255, 0, 0), (75, 200, 50, AX / 2.5 * 200))
    pygame.draw.rect(screen, (255, 0, 0), (150, 200, 50, AY / 2.5 * 200))
    pygame.draw.rect(screen, (255, 0, 0), (225, 200, 50, AZ / 2.5 * 200))

    # compass bars
    pygame.draw.rect(screen, (0, 0, 255), (365, 200, 50, CX / 2000 * 200))
    pygame.draw.rect(screen, (0, 0, 255), (440, 200, 50, CY / 2000 * 200))
    pygame.draw.rect(screen, (0, 0, 255), (515, 200, 50, CZ / 2000 * 200))

    # accelerometer text
    bartext(75, AX, 2.5)
    bartext(150, AY, 2.5)
    bartext(225, AZ, 2.5)

    # compass text
    bartext(365, CX, 2000)
    bartext(440, CY, 2000)
    bartext(515, CZ, 2000)

#    text(555, 366, str(HXY / (2 * math.pi) * 360))
    text(555, 380, str(HXY / (2 * math.pi) * 360))

    # combined acceleration for working out resting gravity
    A = math.fabs(numpy.linalg.norm([AX, AY, AZ]) - 1)
#    print "(%f, %f, %f) - (%f)" % (AX, AY, AZ, A)

    # in a slow moment store most recent direction of the gravitational field
    if A < 0.02:
        GX = AX
        GY = AY
        GZ = AZ
        (PGR, PGA, PGB) = polar(GX, GY, GZ)    

    # acceleration detection for paint strokes (going up reduces gravity to less than one?)
#    A = math.fabs(1 - numpy.sum(numpy.absolute([AX, AY, AZ])))
    text(10, 10, str(A))

#    if A > 0.7 and fast != 1:
    if A > 0.4 and fast != 1:
        fast = 1
        print "fast!"
        print datetime.datetime.now().time()
    elif fast == 1 and A < 0.05:
        fast = 0
        print "slow!"
        print datetime.datetime.now().time()
    elif fast == 1:
#        print "slowing down..."
        # subtract gravity to get direction vector
#        GAX = AX - GX
#        GAY = AY - GY
#        GAZ = AZ - GZ
        (PAR, PAA, PAB) = polar(AX, AY, AZ)
#        print "gravity: %f, %f, %f" % (PGR, PGA, PGB)
#        print "acceleration: %f, %f, %f" % (PAR, PAA, PAB)
        (GAX, GAY, GAZ) = cartesian(PAR, PAA - PGA + PSGA, PAB - PGB + PSGB)
        GAZ = GAZ - PGR # can only subtract proper gravity once it's been translated, other wise parts of the sideways coordinates are subtracted too
#        print "screen gravity: %f, %f, %f" % (GAX, GAY, GAZ)
        pygame.draw.line(screen, (0, 255, 0), (320, 200), (320 + GAY / 2.5 * 200, 200 + GAZ / 2.5 * 200), 2)

    # push updates to the screen
    pygame.display.flip()

    # wait some
    time.sleep(0.005)

pygame.quit()
