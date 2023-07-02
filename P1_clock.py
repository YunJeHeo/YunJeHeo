
import pygame
import numpy as np

def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def getRectangle(width, height, x=0, y=0):
    points = np.array([ [0, 0], 
                        [width, 0], 
                        [width, height], 
                        [0, height]], dtype='float')
    points = points + [x, y]
    return points

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], 
                   [s, c, 0], 
                   [0, 0, 1]], dtype='float')
    return R 

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 

def draw(M, points, color=(0,0,0), p0=None , width=1):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = ( R @ points.T ).T + t 
    pygame.draw.polygon(screen, color, points_transformed, 10)
    if p0 is not None:
        pygame.draw.line(screen, (0,0,0), p0, points_transformed[0], width)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# 색 정의
PURPLE=(100, 10, 150)
GREEN = (100, 200, 100)

pygame.init()  # 1! initialize the whole pygame system!
pygame.display.set_caption("20221138 허윤제")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
sound=pygame.mixer.Sound("assets/bell-ringing-04.mp3")

watch= getRegularPolygon(30, 200)
angle=-90.
angle1=-90.
angle2=-90.

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    angle += 60.
    angle1 += 11
    angle2 += 1
    screen.fill(PURPLE)

    center=(WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
    Mwatch = Tmat(center[0], center[1]) @ Rmat(angle)
    draw(Mwatch, watch, (0, 0, 0), center, 5)

    center=(WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
    Mwatch = Tmat(center[0], center[1]) @ Rmat(angle1)
    draw(Mwatch, watch, (0, 0, 0), center, 15)

    center=(WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
    Mwatch = Tmat(center[0], center[1]) @ Rmat(angle2)
    draw(Mwatch, watch, (0, 0, 0), center, 20)

    if angle2 % 30.==0:
        sound.play()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()