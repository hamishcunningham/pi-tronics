import socket
import select
import pygame
import time
import numpy
import math
import datetime

# port to listen on
port = 5005

# setup networking
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", port))
sock.setblocking(0)

# setup display
pygame.init()
screen = pygame.display.set_mode((640, 400))
myfont = pygame.font.SysFont("sans", 10)

# length of moving average array
AL = 20

# accelerometer storage for moving average
AXa = numpy.zeros((1, AL))
AYa = numpy.zeros((1, AL))
AZa = numpy.zeros((1, AL))

# store gravity when fast is detected..
GX = 0
GY = 0
GZ = 1

# polar gravity
PGR = 0
PGA = -math.pi/2
PGB = 0

# screen gravity
PSGR = 1
PSGA = -math.pi/2
PSGB = 0

# compass storage for moving average
CXa = numpy.zeros((1, AL))
CYa = numpy.zeros((1, AL))
#CZa = numpy.zeros((1, AL))

# accelerometer values
AX = 0
AY = 0
AZ = 0

# rotated for screen accelerometer values
GAX = 0
GAY = 0
GAZ = 0
last_G = 0

# compass values
CX = 0
CY = 0
#CZ = 0

# compass heading
HXY = 0

# compass calibration
MACX = -3000
MICX = 3000
MACY = -3000
MICY = 3000
#MACZ = -3000
#MICZ = 3000

# timing information
last_time = time.time();

# brush info
BX = 0 # position
BY = 0
VX = 0 # velocity
VY = 0
P = 0 # amount of paint on brush

# need a matrix to store splotches in


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
    return (numpy.sum(ARRAY) / l[0], ARRAY)


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
#    x = X * math.sin(B) * math.cos(A)
    x = 0 # don't bother to do the math since we don't use it
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


# ============
# main program
# ============

fast = 0
notfast = 0
running = 1
while running:

    dt = time.time() - last_time
    last_time = time.time()

    # do networking
    result = select.select([sock], [], [], 0)
    if len(result[0]) > 0:
        # read in data
        data = result[0][0].recvfrom(1024)
        a = data[0].split(",")
        AX = float(a[0])
        AY = float(a[1])
        AZ = float(a[2])
        CX = float(a[3])
        CY = float(a[4])
#        CZ = float(a[5])

        # moving averages for acceleration
        (AX, AXa) = movingaverage(AXa, AX)
        (AY, AYa) = movingaverage(AYa, AY)
        (AZ, AZa) = movingaverage(AZa, AZ)

        # combined acceleration for working out resting gravity
        A = math.fabs(numpy.linalg.norm([AX, AY, AZ]) - 1)

        # in a slow moment store most recent direction of the gravitational field
        if A < 0.02 and (last_time - last_G) > 0.12:
            GX = AX
            GY = AY
            GZ = AZ
            (PGR, PGA, PGB) = polar(GX, GY, GZ)
            last_G = last_time

        # rotate to screen coordinates and subtract gravity
        (PAR, PAA, PAB) = polar(AX, AY, AZ)
        (GAX, GAY, GAZ) = cartesian(PAR, PAA - PGA + PSGA, PAB - PGB + PSGB)
        GAY = -GAY
        GAZ = -(GAZ - PGR)

        # moving averages for compass
        (CX, CXa) = movingaverage(CXa, CX)
        (CY, CYa) = movingaverage(CYa, CY)
#        (CZ, CZa) = movingaverage(CZa, CZ)

        # compass calibration
        if CX > MACX:
            MACX = CX
        if CX < MICX:
            MICX = CX
        if CY > MACY:
            MACY = CY
        if CY < MICY:
            MICY = CY
#        if CZ > MACZ:
#            MACZ = CZ
#        if CZ < MICZ:
#            MICZ = CZ

        # https://www.sparkfun.com/products/10619#comment-4f07fe86ce395f5a76000000
        CX = CX - (MACX + MICX) / 2
        CY = CY - (MACY + MICY) / 2
#        CZ = CZ - (MACZ + MICZ) / 2

        # compass heading
        # need to correct CX, CY for tilt of compass...
        # http://www.loveelectronics.co.uk/Tutorials/13/tilt-compensated-compass-arduino-tutorial
        HXY = heading(CX, CY)


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
#    pygame.draw.rect(screen, (0, 0, 255), (515, 200, 50, CZ / 2000 * 200))

    # accelerometer text
    bartext(75, AX, 2.5)
    bartext(150, AY, 2.5)
    bartext(225, AZ, 2.5)

    # compass text
    bartext(365, CX, 2000)
    bartext(440, CY, 2000)
#    bartext(515, CZ, 2000)

    text(555, 380, str(HXY / (2 * math.pi) * 360))

    # acceleration detection for paint strokes
    A = math.fabs(numpy.linalg.norm([GAY, GAZ]))
    text(10, 10, str(A))

    # splotches
    if A > 0.3 and fast != 1:
        fast = 1
        notfast = 0

    if fast == 1:
        if A < 0.08:
            notfast = notfast + dt
            if notfast >= 0.05:
                fast = 0
        pygame.draw.line(screen, (0, 255, 0), (320, 200), (320 + GAY / 2.5 * 200, 200 + GAZ / 2.5 * 200), 2)
        # add a splot spacing relative to A

    # draw the splotches 


    # push updates to the screen
    pygame.display.flip()

    # wait some
    time.sleep(0.005)

pygame.quit()

