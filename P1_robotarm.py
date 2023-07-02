import pygame
import numpy as np

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE=(255, 255, 255)
PURPLE=(100, 10, 150)
YELLOW=(100, 250, 250)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

pygame.init()
pygame.display.set_caption("20221138 허윤제")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


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
    # points = np.array([ [x, y], 
    #                     [x+width, y], 
    #                     [x+width, y+height], 
    #                     [x, y+height]], dtype='float')
    return points
#

center1 = [100., 600.]
angle1 = -20.
width1 = 200
height1 = 100
rect1 = getRectangle(width1, height1)

angle2 = -0.
width2 = 200
height2 = 70
rect2 = getRectangle(width2, height2)

angle3 = 0.
width3 = 30
height3 = 100
rect3 = getRectangle(width3, height3, x=0, y= -height3/2.)

angle4=-40.

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


def draw(M, points, color=(0,0,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = ( R @ points.T ).T + t
    pygame.draw.polygon(screen, color, points_transformed, 2)
    if p0 is not None:
        pygame.draw.line(screen, (0,0,0), p0, points_transformed[0])

def main():
    global angle3, angle2, angle1, angle4
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    done=True
                elif event.key == pygame.K_a:
                    angle1 -= 5.
                elif event.key == pygame.K_b:
                    angle1 += 5.
                elif event.key == pygame.K_LEFT:
                    angle2 -= 5.
                elif event.key == pygame.K_RIGHT:
                    angle2 += 5.
                elif event.key== pygame.K_UP:
                    angle3 -= 5.
                elif event.key==pygame.K_DOWN:
                    angle3 += 5.
                elif event.key==pygame.K_g:
                    angle4 -= 5.
                elif event.key==pygame.K_f:
                    angle4 += 5.


        screen.fill(PURPLE)

        M = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.)
        draw(M, rect1, (0, 255, 250))
        
        M2 = M @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Rmat(angle2) @ Tmat(0, -height1/2.)
        draw(M2, rect1, (255, 0, 255))

        M3 = M2 @ Tmat(width2, 0) @ Tmat(0, height1/2.) @ Rmat(angle3) @ Tmat(0, -height1/2.)
        draw(M3, rect1, (255, 255, 255))

        M4 = M3 @ Tmat(width2, 0) @ Tmat(0, height1/2.) @ Rmat(-angle4) @ Tmat(0, -height1/2.)
        draw(M4, rect3, (0, 0, 0))
        M4 = M3 @ Tmat(width2, 0) @ Tmat(0, height1/2.) @ Rmat(angle4) @ Tmat(0, height1/2.)
        draw(M4, rect3, (0, 0, 0))



        
        pygame.display.flip()
        clock.tick(30)

    pass

if __name__=="__main__":
    main()