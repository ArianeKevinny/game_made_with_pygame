import pygame
import random
from os import path
from functions import *

LARGURA = 640 # Largura da tela
ALTURA = 480

BASE_TILE = 80 #altura do chão

GRAVITY = 5
JUMP_SIZE = BASE_TILE
SPEED_X = 5

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
        self.rect.x = x_frame
        self.rect.bottom = y_frame
        self.speedx = 0
        self.speedy = 0

    def update(self):
    #Atualiza a posição do player.
        
        self.speedy += GRAVITY
        
        if self.speedy > 0:
            self.state = FALLING

        self.rect.y += self.speedy
        
        if self.rect.y == self.rect.bottom:
            if self.speedy > 0:
                self.speedy = 0
                self.state = STILL
            
    def jump(self):
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING

def load_img(img_dir):
    img = {}
    img[PLAYER_IMG] = pygame.image.load(path.join(img_dir, 'galinha.gif')).convert_alpha()
    return img

def movimento_player():

    img = load_img(img_dir)
    player = Player(img[PLAYER_IMG], 80, 400)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                player.jump()
                
    player.update()
