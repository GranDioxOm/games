#! /usr/bin/env python
import pygame, time, random


class Field:
  def __init__(self, sizeField, sizeTile):
    self.size= sizeField #ancho, largo
    self.field = []
    self.sizeTile = sizeTile
    self.backImage = self.createBackground()
    self.initField()
    
  def createBackground(self):
    grass = Nothing(self.sizeTile, COLORGREEN, (0,0))
    back = pygame.Surface(SCREENSIZE)
    print self.size
    for y in range(0, self.size[1]):
      for x in range(0, self.size[0]):
        back.blit(grass.getTile(), (self.sizeTile[0]*x, self.sizeTile[0]*y))

    return back

  def initField(self):
    self.field = [[False for x in range(self.size[1])] for y in range(self.size[0])] 
    for y in range(0, self.size[1]):
      for x in range(0, self.size[0]):
        if (random.randint(1,15) == 1):
          self.field[x][y] = Bush(self.sizeTile, COLORGREEN, (0,0))


    center = (self.size[0]/2, self.size[1]/2)
    for x in range(center[0]-1, center[0]+1):
      for y in range(center[1]-1, center[1]+1):
        self.field[x][y] = False

    self.field[center[0]][center[1]] = Warehouse(self.sizeTile, COLORGREEN, (0,0))
    self.field[center[0]][center[1]+1] = Chofli(self.sizeTile, COLORGREEN, (0,0))

        #else:
        #  self.field[x][y] = Nothing(self.sizeTile, COLORGREEN) 
       
  def drawField(self):
    screen.blit(self.backImage, (0,0))
    for y in range(0, self.size[1]):
      for x in range(0, self.size[0]):
        if self.field[x][y]:
          screen.blit(self.field[x][y].getTile(), (self.sizeTile[0]*x, self.sizeTile[0]*y))

#  def __init__(self):


class Nothing:
  def __init__(self, size, backcolor, pos):
    image = pygame.transform.scale(pygame.image.load('img/nothing.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(backcolor)
    self.tile.blit(image, (0,0))
    self.solid = False
    self.pos = pos

  def getTile(self):
    return self.tile

class Bush:
  def __init__(self, size, backcolor, pos):
    image = pygame.transform.scale(pygame.image.load('img/bush.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(backcolor)
    self.tile.blit(image, (0,0))
    self.solid = True
    self.pos = pos

  def getTile(self):
    return self.tile

class Chofli:
  def __init__(self, size, backcolor, pos):
    image = pygame.transform.scale(pygame.image.load('img/chofli.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(backcolor)
    self.tile.blit(image, (0,0))
    self.solid = True
    self.pos = pos

  def getTile(self):
    return self.tile

class Warehouse:
  def __init__(self, size, backcolor, pos):
    image = pygame.transform.scale(pygame.image.load('img/warehouse.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(backcolor)
    self.tile.blit(image, (0,0))
    self.solid = True
    self.pos = pos

  def getTile(self):
    return self.tile



SCREENSIZE = (600, 600)
MUNDOSIZE = (30,30)
TILESIZE = (SCREENSIZE[0]/MUNDOSIZE[0], SCREENSIZE[1]/MUNDOSIZE[1])


COLORGREEN = (100, 150, 35)
screen = pygame.display.set_mode(SCREENSIZE)
screen.fill(COLORGREEN)

mundo = Field(MUNDOSIZE, TILESIZE)

frame = 0
run = 1
while run:
  #print frame
  #EVENTOS
  event = pygame.event.poll()
  if event.type == pygame.QUIT:
    run = 0

  mundo.drawField()

  pygame.display.update()
  time.sleep(0.01)
  frame+=1