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

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1200
center = (WINDOW_WIDTH / 2., WINDOW_HEIGHT / 2.)

BLACK=(0,0,0)
PURPLE=(100, 10, 150)

pygame.init()
pygame.display.set_caption("Solar System")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def draw(M, points, color=(0,0,0), fill_color=None, p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]
    
    points_transformed = ( R @ points.T ).T + t 
    
    if fill_color is not None:
        pygame.draw.polygon(screen, fill_color, points_transformed)    
    pygame.draw.polygon(screen, color, points_transformed, 5)
    if p0 is not None:
        pygame.draw.line(screen, (0,0,0), p0, points_transformed[0])


Sun = getRegularPolygon(20, 60)
Mercury = getRegularPolygon(10, 10)
Venus = getRegularPolygon(14, 15)
Earth = getRegularPolygon(18, 20)
Moon = getRegularPolygon(18, 4)
Mars = getRegularPolygon(16, 18)
Jupiter = getRegularPolygon(24, 50)
Europa=getRegularPolygon(10, 4)
Ganymede=getRegularPolygon(9, 4)
Saturn = getRegularPolygon(20, 40)
Uranus = getRegularPolygon(16, 30)
Neptune = getRegularPolygon(16, 30)
Asteroid = getRegularPolygon(10, 5)
UFO = getRegularPolygon(4, 3)

Ring = getRegularPolygon(60, 45) 
num_asteroids = 100  # 생성할 소행성의 개수
asteroid_positions = []  # 소행성의 초기 위치를 저장할 리스트
asteroid_angles = np.random.rand(num_asteroids) * 360  # 소행성의 초기 각도를 랜덤으로 설정



dist_mercury = 100
dist_venus = 160
dist_earth = 250
dis_moon= 30
dist_mars = 310
dist_jupiter = 420
dist_saturn = 500
dist_uranus = 600
dist_neptune = 700
dist_asteroid = 370

for i in range(num_asteroids):
    dist = dist_asteroid + np.random.randint(-10, 10)  # 소행성의 초기 거리를 태양에서의 거리에서 조금씩 변동시킴
    angle = asteroid_angles[i]
    asteroid_positions.append((dist, angle))

angle_mercury = 0
angle_venus = 0
angle_earth = 0
angle_moon = 0
angle_moon_sun=0
angle_mars = 0
angle_jupiter = 0
angle_jupiter_G= 0
angle_jupiter_E= 0
angle_saturn = 0
angle_uranus = 0
angle_neptune = 0
angle_asteroid = 0

star_position=[]
for i in range(50):
    x = np.random.randint(0, 1200)
    y = np.random.randint(0, 1000)
    star_position.append( (x, y))

done = False
while not done:
    angle_mercury += 2
    angle_venus += 1.5
    angle_earth += 1
    angle_moon += 3
    angle_moon_sun += 7
    angle_mars += 0.8
    angle_jupiter += 0.4
    angle_jupiter_G += 1
    angle_jupiter_E += 2.5  
    angle_saturn += 0.3
    angle_uranus += 0.2
    angle_neptune += 0.15
    angle_asteroid += 1.2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    for x, y in star_position:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2) 

    for dist, angle in asteroid_positions:
        Masteroid = Tmat(center[0], center[1]) @ Rmat(angle_asteroid+np.random.randint(0, 400)) @ Tmat(dist, 0) @ Rmat(-angle_asteroid) @ Rmat(angle_earth)
        draw(Masteroid, Asteroid, (100, 100, 100), (100, 100, 100), Masteroid[:2, 2])


    Mring = Tmat(center[0], center[1]) @ Rmat(angle_saturn) @ Tmat(dist_saturn, 0) @ Rmat(-angle_saturn) @ Rmat(angle_earth)
    draw(Mring, Ring, (255, 255, 200), (255, 255, 200), Mring[:2, 2])

    center = (WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)

    # 태양
    Msun = Tmat(center[0], center[1]) @ Rmat(angle_asteroid)
    draw(Msun, Sun, (255, 10, 0), (255, 150, 0), center)

    # 수성
    Mmercury = Tmat(center[0], center[1]) @ Rmat(angle_mercury) @ Tmat(dist_mercury, 0) @ Rmat(-angle_mercury) @ Rmat(angle_earth)
    draw(Mmercury, Mercury, (128, 128, 128), (128, 128, 128), Mmercury[:2, 2])

    # 금성
    Mvenus = Tmat(center[0], center[1]) @ Rmat(angle_venus) @ Tmat(dist_venus, 0) @ Rmat(-angle_venus) @ Rmat(angle_earth)
    draw(Mvenus, Venus, (255, 140, 0), (255, 190, 0), Mvenus[:2, 2])

    # 지구
    Mearth = Tmat(center[0], center[1]) @ Rmat(angle_earth) @ Tmat(dist_earth, 0) @ Rmat(-angle_earth) @ Rmat(angle_earth)
    draw(Mearth, Earth, (100, 150, 50), (100, 150, 250), Mearth[:2, 2])

    Mmoon = Mearth @ Rmat(angle_moon_sun) @ Tmat(dis_moon, 0) @ Rmat(angle_moon)
    draw(Mmoon, Moon, (200, 200, 200), (100, 100, 100), Mmoon[:2,2])

    Mufo = Mearth @ Rmat(angle_earth * 2) @ Tmat(30, 0)
    draw(Mufo, UFO, PURPLE, PURPLE, Mufo[:2, 2])

    # 화성
    Mmars = Tmat(center[0], center[1]) @ Rmat(angle_mars) @ Tmat(dist_mars, 0) @ Rmat(-angle_mars) @ Rmat(angle_earth)
    draw(Mmars, Mars, (255, 100, 0), (255, 100, 0), Mmars[:2, 2])

    # 목성
    Mjupiter = Tmat(center[0], center[1]) @ Rmat(angle_jupiter) @ Tmat(dist_jupiter, 0) @ Rmat(-angle_jupiter) @ Rmat(angle_earth)
    draw(Mjupiter, Jupiter, (200, 150, 100), (200, 150, 100), Mjupiter[:2, 2])

    Meuropa = Mjupiter @ Rmat(angle_jupiter_E ) @ Tmat(100, 0) @ Rmat(angle_jupiter)
    draw(Meuropa, Europa, (100, 200, 255), (100, 200, 255), Meuropa[:2, 2])

    Mganymede = Mjupiter @ Rmat(angle_jupiter_G ) @ Tmat(85, 0) @ Rmat(angle_jupiter)
    draw(Mganymede, Ganymede, (200, 200, 200), (200, 200, 200), Mganymede[:2, 2])

    # 토성
    Msaturn = Tmat(center[0], center[1]) @ Rmat(angle_saturn) @ Tmat(dist_saturn, 0) @ Rmat(-angle_saturn) @ Rmat(angle_earth)
    draw(Msaturn, Saturn, (200, 150, 50), (200, 150, 50), Msaturn[:2, 2])

    # 천왕성
    Muranus = Tmat(center[0], center[1]) @ Rmat(angle_uranus) @ Tmat(dist_uranus, 0) @ Rmat(-angle_uranus) @ Rmat(angle_earth)
    draw(Muranus, Uranus, (0, 150, 200), (0, 150, 200), Muranus[:2, 2])

    # 해왕성
    Mneptune = Tmat(center[0], center[1]) @ Rmat(angle_neptune) @ Tmat(dist_neptune, 0) @ Rmat(-angle_neptune) @ Rmat(angle_earth)
    draw(Mneptune, Neptune, (0, 0, 255), (0, 0, 255), Mneptune[:2, 2])

    # 소행성
    Masteroid = Tmat(center[0], center[1]) @ Rmat(angle_asteroid) @ Tmat(dist_asteroid, 0) @ Rmat(-angle_asteroid) @ Rmat(angle_earth)
    draw(Masteroid, Asteroid, (100, 100, 100), (100, 100, 100), Masteroid[:2, 2])

    pygame.display.update()
    clock.tick(60)

pygame.quit()