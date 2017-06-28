#! /usr/bin/env python

import pygame, time
screenSize = (640, 400)
screen = pygame.display.set_mode(screenSize)
run = 1
backcolor = (100, 100, 100)


omSize = (30,30)
om = pygame.image.load('om.png').convert_alpha()

om = pygame.transform.scale(om, omSize)
balon = pygame.Surface(omSize)
balon.fill(backcolor)
balon.blit(om, (0,0))

pos = [0,0]

mov = [3,3]

while run:
  event = pygame.event.poll()
  if event.type == pygame.QUIT:
    run = 0

  if pos[0] + mov[0] + omSize[0] > screenSize[0] or pos[0] + mov[0] < 0:
    mov[0] *= -1

  if pos[1] + mov[1] + omSize[1] > screenSize[1] or pos[1] + mov[1] < 0:
    mov[1] *= -1
  
  pos[0] += mov[0]
  pos[1] += mov[1]

  screen.fill(backcolor)

  screen.blit(om, pos)

  pygame.display.update()
  

  time.sleep(0.01)
