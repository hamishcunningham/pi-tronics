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
    


# screen gravity
(SGX, SGA, SGB) = polar(0, 0, 1)
#print cartesian(SGX, SGA, SGB)
CGSA = 0
CGSB = 0


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
        CX = int(a[3])
        CY = int(a[4])
        CZ = int(a[5])

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

    # combined acceleration
    Atotal = numpy.linalg.norm([AX, AY, AZ])
    A = math.fabs(Atotal - 1)
    text(10, 10, str(A))
#    if A > 0.7 and fast != 1:
    if A > 0.25 and fast != 1:
        fast = 1
        print "fast!"
        print datetime.datetime.now().time()
        GX = gravity(AXa)
        GY = gravity(AYa)
        GZ = gravity(AZa)
#        G = numpy.linalg.norm([GX, GY, GZ])
#        if GZ != 0:
#            (PX, PA, PB) = polar(GX, GY, GZ)
#            CGSA = SGA - PA # current gravity screen rotation A
#            CGSB = SGB - PB
##            print "%f %f %f %f" % (SGA, PA, SGB, PB)
##            print "%f %f" % (CGSA, CGSB)
##            (GX, GY, GZ) = cartesian(PX, CGSA, CGSB)
##            print "gravity: %f, %f, %f" % (GX, GY, GZ)
##            print "%f %f" % (CGSA, CGSB)
    elif fast == 1 and A < 0.05:
        fast = 0
        print "slow!"
        print datetime.datetime.now().time()
    elif fast == 1:
#        print "slowing down..."
        # subtract gravity to get direction vector
        GAX = AX - GX
        GAY = AY - GY
        GAZ = AZ - GZ
##        (PGAX, PGAA, PGAB) = polar(GAX, GAY, GAZ)
#        (PGAX, PGAA, PGAB) = polar(AX, AY, AZ)
#        PGAA = PGAA + CGSA # correct for the screen
#        PGAB = PGAB + CGSB
#        (GAX, GAY, GAZ) = cartesian(PGAX, PGAA, PGAB)
        GAY = GAY * -1
#        GAZ = GAZ - 1
##        print "slowing down... before: %f, %f, %f -- vector: %f, %f, %f" % (AX, AY, AZ, GAX, GAY, GAZ)
        pygame.draw.line(screen, (0, 255, 0), (320, 200), (320 + GAY / 2.5 * 200, 200 + GAZ / 2.5 * 200), 2)

    # push updates to the screen
    pygame.display.flip()

    # wait some
    time.sleep(0.005)

pygame.quit()
