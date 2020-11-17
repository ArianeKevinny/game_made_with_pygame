from functions import *
import pygame


# Classe que comanda os personagens
class Player:
    lives = 3
    num_stars = 0
    nivel = 1

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
        self.player_x = 100  # Posição do personagem no eixo X
        self.counter = 0
        self.jump_counter = 12
        self.char_sprite = insert_gif("animacoes/" + self.char + "/" + self.char +".gif", self.x_scale, self.y_scale)
        self.state = "still"

    def check_fall(self, blocks):
        """Função serve para checar se há algum bloco abaixo do personagem, se olhar todos os blocos e a posição do
        personagem não bater com nenhum bloco, então o personagem irá cair. """
        if self.state == "still" and self.player_y == self.original_y:
            self.state = "falling"
            for block in blocks:
                for b in block.pos_t:
                    if b[0] - math.ceil(self.char_sprite.get_width()/2) <= self.player_x <= b[0] + 40:
                        self.state = "still"

    def show(self, screen, blocks):
        """Função para mostrar o personagem, alterando os frames do gif e executando o pulo"""
        if self.counter == 5:
            self.char_sprite = insert_gif("animacoes/"+ self.char + "/" + self.char + ".gif", self.x_scale, self.y_scale)
            self.counter = 0
        else:
            if self.state == "still" and self.lives > 0:
                self.counter += 1
        screen.blit(self.char_sprite, (self.player_x, self.player_y))
        if self.state == "jumping":
            if self.jump_counter >= -12:
                self.player_y -= round((self.jump_counter * abs(self.jump_counter)) * 0.2)
                self.jump_counter -= 1
            else:
                self.jump_counter = 12
                self.state = "still"
        if self.lives <= 0 or (self.state == "falling" and self.player_y > 480):
            self.state = "dead"

    def jump(self):
        """Função para pular"""
        if self.state == "still":
            self.state = "jumping"
