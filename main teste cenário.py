import pygame
from functions import *
x = 0
blocks = []

pygame.init()
running = True
pygame.display.set_caption("Teste")
screen = pygame.display.set_mode((640, 480))
mode = menu(screen)
print(mode)
if mode == "":
    running = False
else:
    if mode == "city":
        background_pos = [816, [0, 0], [-816, 0]]
    elif mode == "forest":
        background_pos = [1440, [0, 0], [-1440, 0]]
    elif mode == "ice":
        background_pos = [853, [0, 0], [-853, 0]]
    background = pygame.image.load("img/"+mode+"/background.png")
    background = pygame.transform.scale(background, (background_pos[0], 480))
    blocks.append(first_block(mode))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    paralax(screen, background, background_pos)
    for i in range(len(blocks)):
        blocks[i].show(screen)
    if blocks[len(blocks) - 1].create_other:
        block = Block(mode)
        blocks.append(block)
    try:
        if blocks[0].delete:
            blocks.pop(0)
    except:
        pass
    pygame.display.update()
