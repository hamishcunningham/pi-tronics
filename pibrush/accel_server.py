import socket
import select
import pygame
import time
import numpy
import math
import datetime


# ==============
# initialization
# ==============

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
AZa = numpy.ones((1, AL))

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

# accelerometer values
AX = 0
AY = 0
AZ = 0

# rotated for screen accelerometer values
GAX = 0
GAY = 0
GAZ = 0
last_G = 0

# timing information
last_time = time.time();

# brush info
BX = 0 # position
BY = 0
VX = 0 # velocity
VY = 0
P = 0 # amount of paint on brush
last_stroke = 0

# need a matrix to store splotches in
splotches = numpy.zeros((6, 1))


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
    x = 0 # don't bother to do the math since we don't use it
    y = X * math.sin(B) * math.sin(A)
    z = X * math.cos(B)
    return (x, y, z)


# ============
# main program
# ============

fast = 0
notfast = 0
running = 1
while running:

    # move time forward
    dt = time.time() - last_time
    last_time = time.time()

    # check for a quit (or other events at some point I suppose)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    # ====================
    # networking & sensors
    # ====================

    result = select.select([sock], [], [], 0)
    if len(result[0]) > 0:
        # read in data
        data = result[0][0].recvfrom(1024)
        a = data[0].split(",")
        AX = float(a[0])
        AY = float(a[1])
        AZ = float(a[2])

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
        GAZ = GAZ - PGR


    # ==================
    # paintbrush physics
    # ==================

    # acceleration detection for paint strokes
    A = math.fabs(numpy.linalg.norm([GAY, GAZ]))

    # detect moving quickly
    if A > 0.4 and fast != 1 and last_time - last_stroke > 0.5:
        fast = 1
        notfast = 0
        BX = 400 * GAY + 320
        BY = 400 * GAZ + 200
        VX = 0
        VY = 0
        P = 100

    # detect stopping
    if fast == 1 and (A < 0.1 or (BX > (640 + 200) or BX < -200) and (BY > (400 + 200) or BY < -200)) or P <= 0:
        notfast = notfast + dt
        if notfast >= 0.12:
            fast = 0
            BX = 0
            BY = 0
            last_stroke = last_time

    if fast == 1:
        # accelerate the paint brush
        VX = VX - GAY * dt * 150
        VY = VY - GAZ * dt * 150
        BX = BX + VX * dt * 100
        BY = BY + VY * dt * 100

        # add splotches.... high velocity big splotches far apart, low small close
        print splotches


    # =======
    # drawing
    # =======

    # reset to white
    screen.fill((255, 255, 255))

    # accelerometer bars
    pygame.draw.rect(screen, (255, 0, 0), (75, 200, 50, AX / 2.5 * 200))
    pygame.draw.rect(screen, (255, 0, 0), (150, 200, 50, AY / 2.5 * 200))
    pygame.draw.rect(screen, (255, 0, 0), (225, 200, 50, AZ / 2.5 * 200))

    # accelerometer text
    bartext(75, AX, 2.5)
    bartext(150, AY, 2.5)
    bartext(225, AZ, 2.5)

    # draw acceleration vector
    pygame.draw.line(screen, (0, 255, 0), (320, 200), (320 - GAY / 2.5 * 200, 200 - GAZ / 2.5 * 200), 2)

    # draw the paintbrush
    if BX != 0 and BY != 0:
        pygame.draw.circle(screen, (0, 0, 0), (int(BX), int(BY)), 5)



    # draw splotches


    # push updates to the screen
    pygame.display.flip()

    # wait some
    time.sleep(0.004)

pygame.quit()

