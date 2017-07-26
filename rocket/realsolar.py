#! /usr/bin/env python
import pygame, time, random, math


################# CONSTANTS ####################
SCREENSIZE = (500, 500)
BACKCOLOR = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

GRAVITY = 10000

#dist x10e9 m  mas x10e24 kg vel m/s
SUN = {'name':'sun',     'dist':0,    'mass':2000000  'vel':0 }
SS =[ {'name':'mercury', 'dist':58,   'mass':0.36     'vel':47890 },
      {'name':'venus',   'dist':108,  'mass':4.92     'vel':35030 },
      {'name':'earth',   'dist':147,  'mass':6        'vel':29790 },
      {'name':'mars',    'dist':228,  'mass':0.66     'vel':24130 },
      {'name':'jupiter', 'dist':778,  'mass':1908     'vel':13060 },
      {'name':'saturn',  'dist':1429, 'mass':570      'vel':9640  },
      {'name':'urano',   'dist':2871, 'mass':87       'vel':6810  },
      {'name':'neptune', 'dist':4504, 'mass':103.2    'vel':5430  }]



################## CLASSES #######################
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


###################### FUNCTIONS ###############################3

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

 
###################### RUN #################

clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREENSIZE)
window.fill(BACKCOLOR)


screen = Screen(SCREENSIZE, window)  


run = 1
while run:
  #EVENTOS
  event = pygame.event.poll()
  if event.type == pygame.QUIT:
    run = 0




  screen.printScreen()
  pygame.display.update()
  clock.tick(60)
  print clock.get_fps()
