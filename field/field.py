#! /usr/bin/env python
import pygame, time, random


class Field:
  def __init__(self, sizeField, sizeTile):
    self.size= sizeField #ancho, largo
    self.field = []
    self.sizeTile = sizeTile
    self.backImage = self.createBackground()
    self.initField()
    self.rects={}
    self.createRects('food')
    
  def createBackground(self):
    grass = Nothing(self.sizeTile, COLORGREEN, (0,0))
    back = pygame.Surface(SCREENSIZE)
    
    for y in range(0, self.size[1]):
      for x in range(0, self.size[0]):
        back.blit(grass.getTile(), (self.sizeTile[0]*x, self.sizeTile[0]*y))

    return back

  def initField(self):
    for y in range(0, self.size[1]):
      for x in range(0, self.size[0]):
        if (random.randint(1,15) == 1):
          #La posicion que pasamos es el centro de la imagen
          pos = (x*self.sizeTile[0]+self.sizeTile[0]/2,y*self.sizeTile[1]+self.sizeTile[1]/2)
          self.field.append(Bush(self.sizeTile, COLORGREEN, pos))


    center = ((self.size[0]/2)*self.sizeTile[0]+self.sizeTile[0]/2, (self.size[1]/2)*self.sizeTile[1]+self.sizeTile[1]/2)
    self.field.append(Warehouse(self.sizeTile, COLORGREEN, (center)))

    

        #else:
        #  self.field[x][y] = Nothing(self.sizeTile, COLORGREEN) 
       
  def drawField(self):

    screen.blit(self.backImage, (0,0))
    for element in self.field:
      screen.blit(element.getTile(), element.pos)

  def createRects(self, type):
    rect = []
    if type == 'food':
      for element in self.field:
        if element.type == 'food':
          rect.append(element.rect)

      self.rects['food'] = rect
 


class Nothing:
  def __init__(self, size, backcolor, pos):
    image = pygame.transform.scale(pygame.image.load('img/nothing.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(backcolor)
    self.tile.blit(image, (0,0))
    self.solid = False
    self.pos = pos
    self.posTile = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.rect = pygame.Rect(self.posTile, size)

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
    self.posTile = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.rect = pygame.Rect(self.posTile, size)
    self.type = 'food'

  def getTile(self):
    return self.tile

class Chofli:
  def __init__(self, size, backcolor, pos):
    image = pygame.transform.scale(pygame.image.load('img/chofli2.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(backcolor)
    self.tile.blit(image, (0,0))
    self.solid = True
    self.pos = pos
    self.action = 'nothing'
    self.direction = [0, 0]
    self.sizeSearch = 2 * size[0]
    self.posTile = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.rect = pygame.Rect(self.posTile, size)
    self.actualSearch = 0
    self.size = size

  def getTile(self):
    return self.tile

  def moveChofli(self):
    pass

  def doAction(self, field):
    if self.action == 'nothing':
      self.action = 'search_food'
    elif self.action == 'search_food':
      field.createRects('food')
      posinit = (self.posTile[0] - self.actualSearch, self.posTile[1] - self.actualSearch)
      posend = (self.posTile[0] + self.size[0] + self.actualSearch,  self.posTile[1] + self.size[1] + self.actualSearch)
      rectSearch = pygame.Rect(posinit, posend)

      find = False
      for element in field.field:
        if rectSearch.colliderect(element.rect):
          self.direccion = element.pos
          find = True
          break

      if find:
        self.action = 'move'
        self.actualSearch = 0
      else:
        self.actualSearch += 1
    
    elif self.action == 'move':
      dire = self.direction
      pos = self.pos
      mov = [pos[0]-dire[0], pos[1]-dire[1]]
      if mov[0] < 0:
        mov[0] = -1
      elif mov[0] > 0:
        mov[0] = 1

      if mov[1] < 0:
        mov[1] = -1
      elif mov[1] > 0:
        mov[1] = 1

      futpos = (pos[0]+mov[0], pos[1]+mov[1])
      
      touch = False
      for element in field.field:
        if element.rect.collidepoint(futpos):
          self.direccion = element.pos
          touch = True
          break

      #if find:
      #  self.action = 'move'
      #  self.actualSearch = 0
      #else:
      #  self.actualSearch += 1



      self.pos = futpos

      


class Warehouse:
  def __init__(self, size, backcolor, pos):
    image = pygame.transform.scale(pygame.image.load('img/warehouse.png').convert_alpha(), size)
    self.tile = pygame.Surface(size)
    self.tile.fill(backcolor)
    self.tile.blit(image, (0,0))
    self.solid = True
    self.pos = pos
    self.posTile = (pos[0] - size[0]/2, pos[1] - size[1]/2)
    self.rect = pygame.Rect(self.posTile, size)
    self.type = 'building'

  def getTile(self):
    return self.tile

class Tribe:
  def __init__(self):
    self.members = []

  def addMember(self, member):
    self.members.append(member)

  def drawTribe(self):
    for member in self.members:
      screen.blit(member.getTile(), member.pos)

  def actionTribe(self, field):
    for member in self.members:
      member.doAction(field)    



SCREENSIZE = (600, 600)
MUNDOSIZE = (30, 30)
TILESIZE = (SCREENSIZE[0]/MUNDOSIZE[0], SCREENSIZE[1]/MUNDOSIZE[1])
CHOFLISIZE = (15, 15)


#COLORGREEN = (100, 150, 35)
COLORGREEN = (25, 50, 17)

screen = pygame.display.set_mode(SCREENSIZE)
screen.fill(COLORGREEN)

mundo = Field(MUNDOSIZE, TILESIZE)
tribu = Tribe()

center = (mundo.size[0]/2, mundo.size[1]/2)
pos = (center[0]*TILESIZE[0]+TILESIZE[0]/2,(center[1]+1)*TILESIZE[1]+TILESIZE[1]/2)
tribu.addMember(Chofli(CHOFLISIZE, COLORGREEN, pos))

frame = 0
run = 1
while run:
  #print frame
  #EVENTOS
  event = pygame.event.poll()
  if event.type == pygame.QUIT:
    run = 0

  mundo.drawField()
  tribu.drawTribe()
  tribu.actionTribe(mundo)

  pygame.display.update()
  time.sleep(0.01)
  frame+=1