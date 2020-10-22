from functions import *
import pygame


# Classe que comanda os personagens
class Player:
    lives = 3

    def __init__(self, char):
        self.char = char  # Armazena o nome do personagem escolhido
        # Cada personagem possui um tamanho específico como também uma posição, baseada na altura
        if self.char == "galinha":
            self.player_y = 365
            self.original_y = 365
            [self.x_scale, self.y_scale] = [36, 40]
        elif self.char == "pinguim":
            self.player_y = 364
            self.original_y = 364
            [self.x_scale, self.y_scale] = [32, 40]
        elif self.char == "mulher":
            self.player_y = 344
            self.original_y = 344
            [self.x_scale, self.y_scale] = [54, 60]
        else:
            self.player_y = 332
            self.original_y = 332
            [self.x_scale, self.y_scale] = [37, 80]
        self.player_x = 100
        self.counter = 0
        self.jump_counter = 10
        self.char_sprite = insert_gif("animacoes/" + self.char + "/" + self.char +".gif", self.x_scale, self.y_scale)
        self.state = "still"

    def check_fall(self, blocks):
        # print(self.state)
        if self.state == "still" and self.player_y == self.original_y:
            self.state = "falling"
            for block in blocks:
                for b in block.pos_t:
                    if b[0] - math.ceil(self.char_sprite.get_width()/2) <= self.player_x <= b[0] + 40:
                        self.state = "still"

    def show(self, screen, blocks):
        if self.counter == 5:
            self.char_sprite = insert_gif("animacoes/"+ self.char + "/" + self.char + ".gif", self.x_scale, self.y_scale)
            self.counter = 0
        else:
            if self.state == "still" and self.lives > 0:
                self.counter += 1
        screen.blit(self.char_sprite, (self.player_x, self.player_y))
        if self.state == "jumping":
            if self.jump_counter >= -10:
                self.player_y -= (self.jump_counter * abs(self.jump_counter)) * 0.3
                self.jump_counter -= 1
            else:
                self.jump_counter = 10
                self.state = "still"

    def jump(self):
        if self.state == "still":
            self.state = "jumping"
