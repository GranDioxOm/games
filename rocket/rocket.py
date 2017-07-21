#! /usr/bin/env python
import pygame, time, random, math

SCREENSIZE = (600, 600)
BACKCOLOR = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

GRAVITY = 10000



clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREENSIZE)
window.fill(BACKCOLOR)

class Rocket:
  def __init__(self, size, pos):
    #image = pygame.transform.scale(pygame.image.load('img/warehouse.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(RED)
    self.printPos = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.realPos = pos
    self.size = size
    self.direction = (0, 0)
    self.velocity = (0, 0)
    #self.futurePos = (0, 0)

    #self.tile.blit(image, (0,0))
    #self.pos = pos


  def __newPos(self, futurePos):
    self.realPos = futurePos
    self.printPos = (futurePos[0] - self.size[0]/2, futurePos[1] - self.size[1]/2)

  def move(self, vector):
    #si me puedo mover me muevo
    print "vector"
    print vector
    self.direction = sumT(self.direction, vector)
    print "direccion"
    print self.direction

    #self.direction = (self.direction[0], self.direction[1]-GRAVITY)
    #futurePos = (self.realPos[0]+self.direction[0], self.realPos[1]+self.direction[1])
    futurePos = sumT(self.realPos, self.direction)

    self.__newPos(futurePos)




class Planet:
  def __init__(self, size, pos):
    self.tile = pygame.Surface(size)
    self.tile.fill(WHITE)
    self.printPos = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.realPos = pos
    self.size = size



class Screen:
  def __init__(self, size, surface):
    self.size = size
    self.elements = []
    self.surface = surface

  def addElement(self, element):
    self.elements.append(element)

  def printScreen(self):
    #self.surface.fill(BACKCOLOR)
    for element in self.elements:
      self.surface.blit(element.tile, element.printPos)



def calcVector(org, dst):
  #coseno = y
  #seno = x 
  #x = dst[0]-org[0]
  #y = dst[1]-org[1]

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

  #print "direccion:"
  #print  str(dirx) + " - " +  str(diry)

  print "distancia:"
  print math.hypot(x, y)

  Fgrav = GRAVITY/(math.hypot(x, y)*100)**2

  print "fuerza gravedad"
  print Fgrav

  
  velocity = (dirx*Fgrav, diry*Fgrav)

  #print "velocity : "
  #print velocity

  return velocity





def sumT(tup1, tup2):
  return (tup1[0]+tup2[0], tup1[1]+tup2[1])


def minusT(tup1, tup2):
  return (tup1[0]-tup2[0], tup1[1]-tup2[1])

def multT(tup1, tup2):
  return (tup1[0]*tup2[0], tup1[1]*tup2[1])

def divT(tup1, tup2):
  return (tup1[0]/tup2[0], tup1[1]/tup2[1])

rk = Rocket((4, 4), (200, 400))
earth = Planet((20, 20), (300, 300))
screen = Screen(SCREENSIZE, window)

screen.addElement(rk)
screen.addElement(earth)


rk.direction = (2, -3);

#frame = 0
run = 1
while run:
  #print frame
  #EVENTOS
  event = pygame.event.poll()
  if event.type == pygame.QUIT:
    run = 0

  screen.printScreen()
  vector = calcVector(rk.realPos, earth.realPos)
  rk.move(vector)
  


  
  pygame.display.update()
  clock.tick(5)
  #frame+=1
  print clock.get_fps()
