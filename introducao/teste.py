import pygame
import os
from pygame.locals import *

# exit the program
def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

# define display surface
W, H = 600, 480
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("teste")
FPS = 500

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

# load font
fonte = pygame.font.Font(None, 32)
text = 'Ande até o fim do cenário para iniciar.'

bg = pygame.image.load("intro.png").convert()
bgWidth, bgHeight = bg.get_rect().size

stageWidth = bgWidth * 2
stagePosX = 0

startScrollingPosX = HW

circleRadius = 25
circlePosX = circleRadius

playerPosX = circleRadius
playerPosY = 400
playerVelocityX = 0

mulher = [pygame.image.load('mulher1.png'), pygame.image.load('mulher2.png'), pygame.image.load('mulher3.png'),
        pygame.image.load('mulher4.png'), pygame.image.load('mulher5.png'), pygame.image.load('mulher6.png'),
        pygame.image.load('mulher7.png'), pygame.image.load('mulher8.png')]
left = False
right = False
walkcounter = 0
# main loop
while True:
    events()
    pygame.time.delay(65)
    if walkcounter + 1 >= 8:
       walkcounter = 0
    k = pygame.key.get_pressed()

    if k[K_RIGHT]:
        playerVelocityX = +17
        right = True
        left = False
        walkcounter += 1
    elif k[K_LEFT]:
        playerVelocityX = -17
        left = True
        right = False
        walkcounter += 1
    else:
        playerVelocityX = 0
        left = False
        right = False
        walkcounter = 0
    playerPosX += playerVelocityX
    '''if playerPosX > stageWidth - circleRadius: #se o jogador sai pelo limite da direita
        #ir para o menu principal
    '''
    if playerPosX < circleRadius: playerPosX = circleRadius
    if playerPosX < startScrollingPosX:
        circlePosX = playerPosX
    elif playerPosX > stageWidth - startScrollingPosX:
        circlePosX = playerPosX - stageWidth + W
    else:
        circlePosX = startScrollingPosX
        stagePosX += -playerVelocityX

    rel_x = stagePosX % bgWidth
    DS.blit(bg, (rel_x - bgWidth, 0))
    if rel_x < W:
        DS.blit(bg, (rel_x, 0))

    text_surface = fonte.render(text, True, WHITE)
    DS.blit(text_surface, (30,60))
    DS.blit(mulher[walkcounter], (circlePosX - 38, playerPosY - 200))

    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)