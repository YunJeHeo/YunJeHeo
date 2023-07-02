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
rect3 = getRegularPolygon(1000, 20)
rect4 = getRegularPolygon(1000, 20)

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

polygons = []
for i in range(7):
    n = np.random.randint(3, 30)
    r = np.random.randint(3, 30)
    c = np.random.randint(0, 255)
    dx = np.random.randint(0, WINDOW_WIDTH)
    dy = np.random.randint(0, WINDOW_HEIGHT)
    polygon = getRegularPolygon(n, r)
    tpoly = polygon + [dx, dy]
    polygons.append((tpoly, (c, c, c)))

def getRegularPolygonVertices(nv, r):
    v =[]
    for i in range(nv):
       rad= i*2*np.pi/nv
       x=np.cos(rad)*r
       y=np.sin(rad)*r
       v.append([x,y])
    vnp=np.array(v)
    return vnp

class RegularPolygon():
    def __init__(self, nvertices, radius):
        self.nvertices=nvertices
        self.radius=radius
        self.linewidth=np.random.choice([0,3,7])
        self.color=BLACK
        self.p=getRegularPolygonVertices(nvertices, radius)

        self.axy=np.array([0., 0.5])
        self.vxy=np.array([0., 0.])
        self.txy=np.array([0., 0.])

    def update(self,):
        self.vxy += self.axy
        self.txy += self.vxy
        self.q= self.p + self.txy

        if self.txy[0]<self.radius:
            self.vxy *= -1.
        if self.txy[0]+self.radius>WINDOW_WIDTH:
            self.vxy[0] *= -1.
        if self.txy[1]+self.radius>WINDOW_HEIGHT:
            self.vxy[1] *= -1.
            diff= self.txy[1]+self.radius- WINDOW_HEIGHT
            self.txy -= diff
        if self.txy[1]<self.radius:
            self.vxy[1] *= -1.

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.q, width=self.linewidth)
        pygame.draw.line(screen, (10,10,10), self.txy, self.q[0])

class Star(RegularPolygon):
    def __init__(self, radius):
        super().__init__(5, radius)
        self.life_tick = 60
        self.linewidth=1

    def update(self):
        super().update()
        self.color= (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        self.txy += self.vxy
        self.vxy += self.axy
        self.life_tick -= 1
        if self.life_tick < 20:
            self.color = (0, 0, 0)

    def draw(self, screen):
        self.q = self.p + self.txy
        pygame.draw.line(screen, YELLOW, self.q[0], self.q[2])
        pygame.draw.line(screen, WHITE, self.q[1], self.q[3])
        pygame.draw.line(screen, RED, self.q[2], self.q[4])
        pygame.draw.line(screen, BLACK, self.q[3], self.q[0])
        pygame.draw.line(screen, YELLOW, self.q[4], self.q[1])

def create_stars(center, speed):
    star_list = [] 
    for i in range(8): 
        angle= i*360./8.
        rad = np.deg2rad(angle)  
        dx = np.cos(rad) * speed  
        dy = np.sin(rad) * speed  
        star = Star(10)  
        star.txy = center.copy()  
        star.vxy = np.array([dx, dy])  
        star.life_tick=20
        star_list.append(star)
    return star_list

def main():
    global angle3, angle2, angle1, angle4, polygons
    done = False
    while not done:
        star_list=[]
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

        C = M3 @ Tmat(width2, 0) @ Tmat(0, height1/2.)
        center2 = C[0:2, 2]
        pygame.draw.circle(screen, (0,0,0), center2, 5)
        

        M4 = M3 @ Tmat(width2+30, 0) @ Tmat(0, height1/2.) @ Rmat(-angle4) @ Tmat(0, -height1/2.)
        draw(M4, rect3, (0, 0, 0))

        M5 = M3 @ Tmat(width2+30, 0) @ Tmat(0, height1/2.) @ Rmat(angle4) @ Tmat(0, height1/2.)
        draw(M5, rect4, (0, 0, 0))

        for tpoly, color in polygons:
            pygame.draw.polygon(screen, color, tpoly, 5)

        for s in star_list:
            s.update()
            s.life_tick -= 1

        center3 = M4[0:2, 2]
        center4 = M5[0:2, 2]

        polygons_to_remove = []
        for tpoly, color in polygons:
            pygame.draw.polygon(screen, color, tpoly, 5)

            center = np.mean(tpoly, axis=0)
            center_x, center_y = center[0], center[1]
            distance1 = np.linalg.norm(center3 - center)
            distance2 = np.linalg.norm(center4 - center)

            if distance1 < 20 or distance2 < 20:
                polygons_to_remove.append((tpoly, color))
                stars = create_stars(center, 10) 
                star_list.extend(stars)

        for tpoly, color in polygons_to_remove:
            polygons.remove((tpoly, color))
        
        pygame.draw.circle(screen, (0,0,0), center3, 5)
        pygame.draw.circle(screen, (0,0,0), center4, 5)
        
        pygame.draw.line(screen, (0,0,0), center2, center3, 2)
        pygame.draw.line(screen, (0,0,0), center2, center4, 2)


        star_list=[s for s in star_list if s.life_tick >0]


        for star in star_list:
            star.draw(screen)



        
        pygame.display.flip()
        clock.tick(30)

    pass

if __name__=="__main__":
    main()