from Blocks import Block
import pygame

x = 0
blocks = []
mode = "forest"

def first_block():
    b = Block(mode)
    b.num = 20
    b.pos_top = []
    b.pos_bottom = []
    for i in range(b.num):
        b.pos_top.append([i * 32, 408])
        b.pos_bottom.append([i * 32, 444])
    blocks.append(b)

def paralax(screen):
    screen.blit(background, background_pos[1])
    screen.blit(background, background_pos[2])
    background_pos[1][0] += 1
    background_pos[2][0] += 1
    if background_pos[1][0] == background_pos[0]:
        background_pos.pop(1)
        background_pos.append([-background_pos[0], 0])

def new_block():
    block = Block(mode)
    blocks.append(block)

pygame.init()
running = True
pygame.display.set_caption("Teste")
screen = pygame.display.set_mode((640, 480))
first_block()

if mode == "city":
    background_pos = [816, [0, 0], [-816, 0]]
elif mode == "forest":
    background_pos = [1440, [0, 0], [-1440, 0]]
elif mode == "ice":
    background_pos = [853, [0, 0], [-853, 0]]
background = pygame.image.load("img/"+mode+"/background.png")
background = pygame.transform.scale(background, (background_pos[0], 480))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    paralax(screen)
    for i in range(len(blocks)):
        blocks[i].show(screen)
    if blocks[len(blocks) - 1].create_other:
        new_block()
    try:
        if blocks[0].delete:
            blocks.pop(0)
    except:
        pass
    pygame.display.update()
