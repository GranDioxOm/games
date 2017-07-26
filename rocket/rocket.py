#! /usr/bin/env python
import pygame, time, random, math

SCREENSIZE = (600, 600)
BACKCOLOR = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

GRAVITY = 10000



clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREENSIZE)
window.fill(BACKCOLOR)

class Rocket:
  def __init__(self, size, pos, color, screen):
    #image = pygame.transform.scale(pygame.image.load('img/warehouse.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(color)
    self.printPos = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.realPos = pos
    self.size = size
    self.direction = (0, 0)
    self.velocity = (0, 0)
    screen.addElement(self)
    #self.futurePos = (0, 0)

    #self.tile.blit(image, (0,0))
    #self.pos = pos


  def __newPos(self, futurePos):
    self.realPos = futurePos
    self.printPos = (futurePos[0] - self.size[0]/2, futurePos[1] - self.size[1]/2)

  def move(self, vector):
    #si me puedo mover me muevo
    #print "vector"
    #print vector
    self.direction = sumT(self.direction, vector)
    #print "direccion"
    #print self.direction

    #self.direction = (self.direction[0], self.direction[1]-GRAVITY)
    #futurePos = (self.realPos[0]+self.direction[0], self.realPos[1]+self.direction[1])
    futurePos = sumT(self.realPos, self.direction)

    self.__newPos(futurePos)




class Planet:
  def __init__(self, size, pos, soi, screen):
    self.tile = pygame.Surface(size)
    pygame.draw.circle(self.tile, WHITE, (size[0]/2, size[1]/2), size[0]/2)
    self.printPos = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.realPos = pos
    self.size = size
    screen.addElement(self)
    self.soi = soi
    self.direction = (0, 0)
    self.moons = []

  def move(self, vector):
    self.direction = sumT(self.direction, vector)
    futurePos = sumT(self.realPos, self.direction)
    self.__newPos(futurePos)

  def __newPos(self, futurePos):
    self.realPos = futurePos
    self.printPos = (futurePos[0] - self.size[0]/2, futurePos[1] - self.size[1]/2)


class Sun:
  def __init__(self, size, pos, screen):
    self.tile = pygame.Surface(size)
    pygame.draw.circle(self.tile, YELLOW, (size[0]/2, size[1]/2), size[0]/2)
    self.printPos = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.realPos = pos
    self.size = size
    screen.addElement(self)

class Moon:
  def __init__(self, size, pos, screen):
    self.tile = pygame.Surface(size)
    pygame.draw.circle(self.tile, WHITE, (size[0]/2, size[1]/2), size[0]/2)
    self.printPos = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.realPos = pos
    self.size = size
    screen.addElement(self)
    self.direction = (0, 0)

  def move(self, vector):
    self.direction = sumT(self.direction, vector)
    futurePos = sumT(self.realPos, self.direction)

    self.__newPos(futurePos)

  def __newPos(self, futurePos):
    self.realPos = futurePos
    self.printPos = (futurePos[0] - self.size[0]/2, futurePos[1] - self.size[1]/2)

    
class Screen:
  def __init__(self, size, surface):
    self.size = size
    self.elements = []
    self.surface = surface

  def addElement(self, element):
    self.elements.append(element)

  def printScreen(self):
    self.surface.fill(BACKCOLOR)
    for element in self.elements:
      self.surface.blit(element.tile, element.printPos)




def calcVector(org, dst):
  xy = minusT(dst, org)
  x = xy[0]
  y = xy[1]

  if xy[0] < 0:
    x *= -1
  if xy[1] < 0:
    y *= -1

  tot = x + y

  dirx = x/tot
  diry = y/tot

  if xy[0] < 0:
    dirx *= -1
  if xy[1] < 0:
    diry *= -1

  #Fuerza de la gravedad
  Fgrav = GRAVITY/(math.hypot(x, y)*100)#**2
  velocity = (dirx*Fgrav, diry*Fgrav)
  return velocity


def calcDist(pos1, pos2):
  xy = minusT(pos1, pos2)
  print xy
  dist = math.hypot(xy[0], xy[1])
  #print dist
  return dist


def sumT(tup1, tup2):
  return (tup1[0]+tup2[0], tup1[1]+tup2[1])


def minusT(tup1, tup2):
  return (tup1[0]-tup2[0], tup1[1]-tup2[1])

def multT(tup1, tup2):
  return (tup1[0]*tup2[0], tup1[1]*tup2[1])

def divT(tup1, tup2):
  return (tup1[0]/tup2[0], tup1[1]/tup2[1])

def createRk():
  rk = Rocket((4, 4), mouseInit, RED, screen)
  initVector = minusT(mouseEnd, mouseInit)
  rk.direction = initVector
  rockets.append(rk)
  
  

planets = []
rockets = []
screen = Screen(SCREENSIZE, window)
#rk = Rocket((4, 4), (100, 100), RED, screen)
#rk2 = Rocket((4, 4), (200, 300), BLUE, screen)
sun = Sun((20,20), (SCREENSIZE[0]/2, SCREENSIZE[1]/2), screen)
earth = Planet((10, 10), (250, 300), 0, screen)
mars = Planet((10, 10), (200, 300), 0, screen)
saturn = Planet((10, 10), (150, 300), 0, screen)
jupiter = Planet((10, 10), (100, 300), 0, screen)
luna1 = Moon((5, 5), (115, 300), screen)

planets.append(earth)
planets.append(mars)
planets.append(saturn)
planets.append(jupiter)
jupiter.moons.append(luna1)



#rk.direction = (0, -10)
#rk2.direction = (10, -10)
earth.direction = (0, -8.7)
mars.direction = (0, -8.7)
saturn.direction = (0, -8.7)
jupiter.direction = (0, -8.7)
luna1.direction = (0, 1.5)

mouseInit = (0,0)
mouseEnd = (0,0)
#frame = 0
run = 1
while run:
  #print frame
  #EVENTOS
  event = pygame.event.poll()
  #print event.type
  if event.type == pygame.QUIT:
    run = 0
  elif event.type == pygame.MOUSEBUTTONDOWN:
    mouseInit = pygame.mouse.get_pos()
  elif event.type == pygame.MOUSEBUTTONUP:
    mouseEnd = pygame.mouse.get_pos()
    
    #createRk()
    mouseInit = (0,0)
    mouseEnd = (0,0)
  #elif event.type == pygame.MOUSEMOTION:
  #  if mouse == True:
  #    print "move move move"

  
  #if earth.soi >= calcDist(rk.realPos, earth.realPos):
  #  print "cerca tierra"
  #  vector = calcVector(rk.realPos, earth.realPos)
  #elif mars.soi >= calcDist(rk.realPos, mars.realPos):
  #  print "cerca marte"
  #  vector = calcVector(rk.realPos, mars.realPos)
  #else:
  #  vector = calcVector(rk.realPos, (300,300))

  #vector1 =  calcVector(rk.realPos, earth.realPos)
  #vector2 =  calcVector(rk.realPos, mars.realPos)
  #vector = sumT(vector1, vector2)

  #rk.move(vector)
  #vector1 =  calcVector(rk2.realPos, earth.realPos)
  #vector2 =  calcVector(rk2.realPos, mars.realPos)
  #vector = sumT(vector1, vector2)
  #rk2.move(vector)


  #vector = calcVector(rk2.realPos, earth.realPos)
  #rk2.move(vector)
  
  #print pygame.mouse.get_pressed()
  #print pygame.event.wait()
  #print pygame.event.get()

  #for rk in rockets:
  #  vector1 =  calcVector(rk.realPos, earth.realPos)
  #  vector2 =  calcVector(rk.realPos, mars.realPos)
  #  vector = sumT(vector1, vector2)
  #  rk.move(vector)
  
  for planet in planets:
    vector = calcVector(planet.realPos, sun.realPos)
    planet.move(vector)
    if len(planet.moons) > 0:
      for moon in planet.moons:
        vector = calcVector(moon.realPos, planet.realPos)
        moon.move(vector)

  screen.printScreen()
  pygame.display.update()
  clock.tick(60)
  #frame+=1
  print clock.get_fps()
