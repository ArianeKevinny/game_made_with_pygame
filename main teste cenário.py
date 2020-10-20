import pygame
from functions import *

blocks = []  # Lista em que serão armazenados os blocos que aparecem na tela

pygame.init()
running = True
pygame.display.set_caption("Teste")  # Título do jogo
screen = pygame.display.set_mode((600, 480))  # Tamanho da tela
[mode, char] = menu(screen)  # Mostra o menu
print(mode)     
if mode == "":
    running = False
else:
    # Os papéis de parede possuem diferentes tamanhos, então é preciso adaptar o tamanho para cada um deles
    if mode == "city":
        background_pos = [816, [0, 0], [-816, 0]]
    elif mode == "forest":
        background_pos = [1440, [0, 0], [-1440, 0]]
    elif mode == "ice":
        background_pos = [853, [0, 0], [-853, 0]]
    background = pygame.image.load("img/"+mode+"/background.png")  # Carrega o papel de parede
    background = pygame.transform.scale(background, (background_pos[0], 480))  # Adequa para caber na tela
    blocks.append(first_block(mode))  # O primeiro bloco é maior que a maioria
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    paralax(screen, background, background_pos)
    for i in range(len(blocks)):
        blocks[i].show(screen)
    if blocks:
        if blocks[len(blocks) - 1].create_other:
            block = Block(mode)
            blocks.append(block)
        if blocks[0].delete:
            del blocks[0]
    pygame.display.update()
