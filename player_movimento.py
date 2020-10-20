import pygame
import random
from os import path

LARGURA = 640 # Largura da tela
ALTURA = 480

BASE_TILE = 80 #altura do chão (não sei o valor)

GRAVITY = 5
JUMP_SIZE = BASE_TILE
SPEED_x = 5

STILL = 0
JUMPING = 1
FALLING = 2

img_dir = path.join(path.dirname(__file__), 'animações')
PLAYER_IMG = 'player_img'

class player(pygame.sprite.Sprite):
    def __init__(self, player_img, x_frame, y_frame):
        pygame.sprite.Sprite.__init__(self)
        self.state = STILL
        self.image = player_img
        self.rect = self.image.get_rect()
        #self.rect.x = y_frame    (Não sei onde posicionar o personagem inicialmente)
        #self.rect.bottom = x_frame era disso que eu me referi a falar de 'Base'
        self.speedx = 0
        self.speedy = 0

    def update(self):
    #Atualiza a posição do player.

        #Andar em Y
        self.speedy += GRAVITY
        self.rect.y += self.speedy
        if self.speedy > 0:
            self.state = FALLING        
        
        #Andar em X
        self.rect.x += self.speedx
        #N passar da janela
        if self.rect.left < 0:
            self.rect.left = 0;
        if self.rect.rigth >= LARGURA:
            self.rect.rigth = LARGURA - 1

    def jump(self):
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING

def load_img(img_dir):
    img = {}
    img[PLAYER_IMG] = pygame.image.load(path.join(img_dir, 'galinha.gif')).convert_alpha()
    return img

def keys():

    img = load_img(img_dir)
    player = Player(img[PLAYER_IMG], x_frame, y_frame) 
        #(X_FRAME,-Y_FRAME)substituir pela posição inicial do jogador

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx -= SPEED_X
            elif event.key == pygame.K_RIGHT:
                player.speedx += SPEED_X
            elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                player.jump()
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.speedx += SPEED_X
            elif event.key == pygame.K_RIGHT:
                player.speedx -= SPEED_X

    player.update()
